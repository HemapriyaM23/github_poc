#Version = 1.0
#Updated Date = 7-JULY-2025
#Created by = Soumik

import glob
import os
import time
import fnmatch
from .general import General
from .aws import EC2Operation,S3Operation

class ArchivePurge():

    @classmethod
    def upload_files(self):
        try:
            for item in General.var_archive_purge_values:
                
                General.logger.info(f'Source Path: {item.get("SOURCE_DIR")} Pattern: {item.get("FILE_PATTERN")}')
                files = glob.glob(os.path.join(item.get("SOURCE_DIR"), item.get("FILE_PATTERN")))
                
                if item.get("EXCLUDE_FILE_PATTERN"):
                    excluded_files = set(glob.glob(os.path.join(item.get("SOURCE_DIR"), item.get("EXCLUDE_FILE_PATTERN"))))
                    filtered_files = [f for f in files if f not in excluded_files]
                else:
                    filtered_files = files

                
                if not filtered_files:
                    General.logger.info(f'No files matching pattern: {item.get("FILE_PATTERN")} and exclude {item.get("EXCLUDE_FILE_PATTERN")}')
                    continue

                for file_path in filtered_files:
                    filename = os.path.basename(file_path)
                    S3Operation.upload_file_to_s3(file_path, filename, item.get("BUCKET_NAME"), item.get("TARGET_DIR"))
                    EC2Operation.delete_from_ec2(file_path)
                    General.logger.info(f'Archive file {file_path} from EC2 to {item.get("BUCKET_NAME")}/{item.get("TARGET_DIR")}')
        except Exception as e:
            General.logger.info(f'Failed to Archive file from EC2 to S3 : {e}')
            raise

    @classmethod
    # function to delete file from EC2
    def purge_local_files(self):
        try:
            current_time = time.time()
            
            for item in General.var_archive_purge_values:

                General.logger.info(f'Target Path: {item.get("TARGET_DIR")} Pattern: {item.get("FILE_PATTERN")}')
                files = glob.glob(os.path.join(item.get("TARGET_DIR"), item.get("FILE_PATTERN")))
            
                if item.get("EXCLUDE_FILE_PATTERN"):
                    excluded_files = set(glob.glob(os.path.join(item.get("TARGET_DIR"), item.get("EXCLUDE_FILE_PATTERN"))))
                    filtered_files = [f for f in files if f not in excluded_files]
                else:
                    filtered_files = files

                for file_path in filtered_files:

                    file_age_in_days = (current_time - os.path.getmtime(file_path)) / (60 * 60 * 24)  # Days

                    General.logger.info(f'File Path: {file_path}, file_age_in_days: {int(file_age_in_days)}')
                
                    if int(file_age_in_days) > int(item.get("EC2_RETENTION_PERIOD_IN_DAYS")):
                        EC2Operation.delete_from_ec2(file_path)
                        General.logger.info(f'Purged file {file_path} from EC2 (older than {item.get("EC2_RETENTION_PERIOD_IN_DAYS")} days)')
        except Exception as e:
            General.logger.info(f"Failed to purge files from EC2: {e}")
            raise

    
    @classmethod
    # function to delete file from S3
    def purge_s3_files(self):
        try:

            for item in General.var_archive_purge_values:

                General.logger.info(f'Bucket Name: {item.get("BUCKET_NAME")} Target Path: {item.get("TARGET_DIR")} Pattern: {item.get("FILE_PATTERN")}')
                # List all files in the target S3 directory
                files = S3Operation.get_s3_file_list_with_modifieddate(item.get("BUCKET_NAME"),item.get("TARGET_DIR"))
                
                for file, last_modified in files:
                    
                    if fnmatch.fnmatch(os.path.basename(file),item.get("FILE_PATTERN")) and (not item.get("EXCLUDE_FILE_PATTERN") or not fnmatch.fnmatch(os.path.basename(file), item.get("EXCLUDE_FILE_PATTERN"))):
                        
                        file_age_in_days = int((time.time() - last_modified.timestamp()) / (60 * 60 * 24))  # Days
                        
                        if file_age_in_days > int(item.get("S3_RETENTION_PERIOD_IN_DAYS")):
                            S3Operation.delete_s3_object(item.get("BUCKET_NAME"),file)
                            General.logger.info(f'Purged file {file} from S3 (older than {item.get("S3_RETENTION_PERIOD_IN_DAYS")} days)')
        except Exception as e:
            General.logger.info(f"Failed to purge files from S3: {e}")
            raise

def test_purge_old_archives(target_dir, days):
    """Purge files older than 'days' from the target directory."""
    current_time = time.time()
    deleted_count = 0

    for dirpath, dirnames, filenames in os.walk(target_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_age_in_days = (current_time - os.path.getmtime(file_path)) / (60 * 60 * 24)  # Days
            
            if int(file_age_in_days) > days:
                os.remove(file_path)
                deleted_count += 1

    return deleted_count

def test_purge_old_archives_removes_old_files():
    """Test that purge_old_archives removes files older than the specified days."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file older than 5 days
        old_file = os.path.join(temp_dir, "old.txt")
        with open(old_file, "w") as f:
            f.write("old file")
        # Set the modification time to 10 days ago
        old_time = time.time() - (10 * 24 * 60 * 60)
        os.utime(old_file, (old_time, old_time))

        # Create a file newer than 5 days
        new_file = os.path.join(temp_dir, "new.txt")
        with open(new_file, "w") as f:
            f.write("new file")
        # Set the modification time to 2 days ago
        new_time = time.time() - (2 * 24 * 60 * 60)
        os.utime(new_file, (new_time, new_time))

        # Run the purge function
        deleted_count = purge_old_archives(temp_dir, 5)

        # Assert only the old file was deleted
        assert deleted_count == 1
        assert not os.path.exists(old_file)
        assert os.path.exists(new_file)
