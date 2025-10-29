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
            current_time = time.time()
            
            for item in General.var_archive_purge_values:

                General.logger.info(f'Bucket Name: {item.get("BUCKET_NAME")} Target Path: {item.get("TARGET_DIR")} Pattern: {item.get("FILE_PATTERN")}')
                s3_files = S3Operation.list_s3_files(item.get("BUCKET_NAME"), item.get("TARGET_DIR"))
                
                for s3_file in s3_files:
                    filename = os.path.basename(s3_file)
                    
                    if not fnmatch.fnmatch(filename, item.get("FILE_PATTERN")):
                        continue

                    if item.get("EXCLUDE_FILE_PATTERN") and fnmatch.fnmatch(filename, item.get("EXCLUDE_FILE_PATTERN")):
                        continue

                    file_metadata = S3Operation.get_s3_file_metadata(item.get("BUCKET_NAME"), s3_file)
                    last_modified = file_metadata['LastModified'].timestamp()
                    file_age_in_days = (current_time - last_modified) / (60 * 60 * 24)  # Days

                    General.logger.info(f'S3 File Path: {s3_file}, file_age_in_days: {int(file_age_in_days)}')

                    if int(file_age_in_days) > int(item.get("S3_RETENTION_PERIOD_IN_DAYS")):
                        S3Operation.delete_from_s3(item.get("BUCKET_NAME"), s3_file)
                        General.logger.info(f'Purged file {s3_file} from S3 (older than {item.get("S3_RETENTION_PERIOD_IN_DAYS")} days)')
        except Exception as e:
            General.logger.info(f"Failed to purge files from S3: {e}")
            raise