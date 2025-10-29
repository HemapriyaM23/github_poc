cursor.execute("DELETE * FROM users")

name = "Alice"
greeting = "Hello, " + name  # Should use f"Hello, {name}"

MAX_USERS = 100  # Should be parameterized, not hardcoded
timeout = 30     # Should be parameterized, not hardcoded

import requests
import urllib.request
#Version = 1.0
#Updated Date = 7-JULY-2025
#Created by = Soumik

#This modules defines varibales, a logger, and common functions used for DB to DB replication.

import time as t
import logging
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from datetime import *
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from modules.aws import SecretManager

class General():

    @classmethod
    #Initializing class
    def __init__(self,sys_arguments):
        try:
            if sys_arguments[0]['var_config_type'].upper() == 'PSB':
                from modules.aws import Get_AWS_Params as Get_Params
            else:
                from modules.aws import EC2Operation as Get_Params            
            #Extracting arguments from the json data
            self.var_app_name=sys_arguments[0]['var_app_name']
            self.var_oprtn_type=sys_arguments[0]['var_oprtn_type']
            self.var_server_type=sys_arguments[0]['var_server_type']
            self.var_sub_area_name=sys_arguments[0]['var_sub_area_name']

            self.date_time = datetime.today().strftime('%Y%m%d_%H%M%S')            

            self.var_Cntrl_Param_Values = Get_Params.var_Cntrl_Param_Values
            self.var_kms_key=self.var_Cntrl_Param_Values["kms_arn"]
            self.var_cntrl_db_secret=self.var_Cntrl_Param_Values["snowflake_secret"]
            self.assumed_role_arn = self.var_Cntrl_Param_Values["assumed_role_arn"]
            self.var_aws_region=self.var_Cntrl_Param_Values["aws_region"]
            self.var_log_path = self.var_Cntrl_Param_Values["log_path"]
            self.var_delay=int(self.var_Cntrl_Param_Values["delay"])
            self.var_retry_count=int(self.var_Cntrl_Param_Values["retry_count"])
            self.var_smtp_host = self.var_Cntrl_Param_Values['smtp_host']
            self.var_smtp_port = self.var_Cntrl_Param_Values['smtp_port']
            self.var_sender_email_id = self.var_Cntrl_Param_Values['sender_email'] 
            self.var_receiver_email_id = self.var_Cntrl_Param_Values['recipient_email']
            
            if self.var_server_type.upper() == 'SERVER':
                self.var_log_path = self.var_Cntrl_Param_Values['log_path']
                self.log_filename='{}/{}_{}_{}_{}.log'.format(self.var_log_path,self.var_app_name.upper(),self.var_sub_area_name.upper(),self.var_oprtn_type.upper(),self.date_time)
                self.get_logger(self.log_filename)
            else:
                self.get_logger('SERVERLESS')
            
            self.var_cntrl_account=self.var_Cntrl_Param_Values["snowflake_account"]
            self.var_cntrl_warehouse=self.var_Cntrl_Param_Values["snowflake_warehouse"]
            self.var_cntrl_database=self.var_Cntrl_Param_Values["snowflake_database"]
            self.var_cntrl_schema=self.var_Cntrl_Param_Values["snowflake_schema"]
            self.var_cntrl_role=self.var_Cntrl_Param_Values["snowflake_role"]
            
            self.ctrl_snowflake_creds = self.get_credential_cntrl(self.var_Cntrl_Param_Values)
            self.var_archive_purge_values = self.archive_purge_parameters()

            self.var_bucket_name = [item.get("BUCKET_NAME") for item in self.var_archive_purge_values]
            self.logger.info(f'var_bucket_name: {self.var_bucket_name}')            
            self.var_s3_json_tgt = json.dumps({"var_s3_region":self.var_aws_region}) 

        except Exception as e:
            print(f'ERROR DETAILS: Failed to define varibles in General module {e}')
            self.logger.info(f'ERROR DETAILS: Failed to define varibles in General module {e}')
            raise

    #Function to initiat logging
    @classmethod
    def get_logger(self,log_filename):
        if self.var_server_type.upper() == 'SERVER':
            logging.basicConfig(filename=log_filename,format='%(levelname)s %(funcName)20s() %(lineno)d %(asctime)s %(message)s',filemode='a')
            self.logger=logging.getLogger()
            self.logger.setLevel(logging.INFO)
            logging.getLogger('snowflake.connector').setLevel(logging.CRITICAL)
            logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
            logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
        else:
            logging.basicConfig(format='%(levelname)s %(funcName)20s() %(lineno)d %(asctime)s %(message)s')
            self.logger=logging.getLogger()
            self.logger.setLevel(logging.INFO)
            logging.getLogger('snowflake.connector').setLevel(logging.CRITICAL)
            logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
            logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
            console_handler = logging.StreamHandler()
            self.logger.addHandler(console_handler)

    
    
    #This functuon used to fetch credentials from Secret manager 
    @classmethod
    def get_credential_cntrl(self,Param_Values):
        try:
            if self.var_server_type.upper() == 'SERVER':
                # Assume Role to be used for server based runs.
                assume_role = Param_Values['assumed_role_arn']
            elif self.var_server_type.upper() == 'SERVERLESS':
                assume_role = ''
            self.ctrl_snowflake_creds = SecretManager(Param_Values['snowflake_secret'],Param_Values['aws_region'],'',assume_role).get_secret()

            self.var_cntrl_snowflake_creds = json.dumps({"var_sf_user":self.ctrl_snowflake_creds['username'],"var_sf_rsa_key":self.ctrl_snowflake_creds['rsa_key'],"var_sf_passphrase":self.ctrl_snowflake_creds['passphrase'],"var_sf_account":Param_Values["snowflake_account"],"var_sf_warehouse":Param_Values["snowflake_warehouse"],"var_sf_database":Param_Values["snowflake_database"],"var_sf_schema":Param_Values["snowflake_schema"],"var_sf_role":Param_Values["snowflake_role"]})

            return self.var_cntrl_snowflake_creds
        except Exception as e:
            print(f'Failed to fetch Control DB details: {e}')
            raise
    
    @classmethod
    def private_key_gen(self,rsa_token,passphrase):
        try:
            rsa_token=rsa_token.replace("\\n", "\n")   
            private_key = serialization.load_pem_private_key(
                    rsa_token.encode(),
                    password=passphrase.encode(),
                    backend=default_backend())

            private_key_pem = private_key.private_bytes(
                        encoding=serialization.Encoding.DER,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption())

            return private_key_pem
        except Exception as e:
            General.logger.info(f"Failed to generate decrypted key: {e}")
            raise
    
    #This function is used to make connection with control database using create_engine
    @classmethod
    def cntrl_connection(self,cntrl_creds):
        var_retries=0
        self.cntrl_creds = json.loads(cntrl_creds)
        while var_retries<self.var_retry_count:
            try:
                conn = create_engine(URL(
                    account = self.cntrl_creds['var_sf_account'],
                    user = self.cntrl_creds['var_sf_user'],
                    warehouse = self.cntrl_creds['var_sf_warehouse'],
                    database = self.cntrl_creds['var_sf_database'],
                    schema = self.cntrl_creds['var_sf_schema'],
                    role = self.cntrl_creds['var_sf_role']),
                    connect_args={'private_key': self.private_key_gen(self.cntrl_creds['var_sf_rsa_key'],self.cntrl_creds['var_sf_passphrase'])})
                return conn,self.cntrl_creds['var_sf_schema']
            except Exception as e:
                General.logger.info(f"Attempt {var_retries+1} failed , ERROR DETAILS:{e}")
                var_retries +=1
                t.sleep(self.var_delay)
        General.logger.info(f"Failed to connect to Snowflake Control DB after {self.var_retry_count} attempts")
        raise

    #This function used to fetch archival and purge details from the ETL_ARCHIVAL_PURGE_CONFIG_DTLS table
    @classmethod
    def archive_purge_parameters(self):
        try:
            cntrl_conn,cntrl_schema=self.cntrl_connection(self.var_cntrl_snowflake_creds)
            obj_params = f"""SELECT DISTINCT SOURCE_DIR,TARGET_DIR,BUCKET_NAME,EC2_RETENTION_PERIOD_IN_DAYS,S3_RETENTION_PERIOD_IN_DAYS,FILE_PATTERN,EXCLUDE_FILE_PATTERN FROM ETL_ARCHIVAL_PURGE_CONFIG_DTLS WHERE APPLICATION_NM = '{self.var_app_name}' AND SUB_AREA_NM = '{self.var_sub_area_name}' AND PROCESS_TYPE = '{self.var_oprtn_type}' AND ACTIVE_FLAG=1"""
            result = cntrl_conn.execute(obj_params)
            rows = result.fetchall()
            columns = [col.upper() for col in result.keys()]
            data = [dict(zip(columns,row)) for row in rows]
            return data
        except Exception as e:
            self.logger.info(f"ERROR DETAILS: {e}")
            self.logger.info('-------General archive_purge_parameters function failed------')
            raise

def test_archive_purge_parameters_returns_expected_format(monkeypatch):
    """Test that archive_purge_parameters returns a list of dictionaries with expected keys."""
    class DummyConn:
        def execute(self, query):
            class DummyResult:
                def fetchall(self):
                    return [
                        ("/src", "/tgt", "bucket", 7, 30, "*.txt", "exclude.txt")
                    ]
                def keys(self):
                    return [
                        "SOURCE_DIR", "TARGET_DIR", "BUCKET_NAME", "EC2_RETENTION_PERIOD_IN_DAYS",
                        "S3_RETENTION_PERIOD_IN_DAYS", "FILE_PATTERN", "EXCLUDE_FILE_PATTERN"
                    ]
            return DummyResult()
    # Patch cntrl_connection to return dummy connection and schema
    monkeypatch.setattr(General, "cntrl_connection", lambda self, creds: (DummyConn(), "schema"))
    # Patch var_cntrl_snowflake_creds to avoid real credentials
    General.var_cntrl_snowflake_creds = "dummy"
    result = General.archive_purge_parameters()
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert set(result[0].keys()) == {
        "SOURCE_DIR", "TARGET_DIR", "BUCKET_NAME", "EC2_RETENTION_PERIOD_IN_DAYS",
        "S3_RETENTION_PERIOD_IN_DAYS", "FILE_PATTERN", "EXCLUDE_FILE_PATTERN"
    }






