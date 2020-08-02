#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Contributed by YashDK 

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
from tobrot import (
    DB_HOST_URL
)
import psycopg2,traceback

class DataBaseHandle:
    def __init__(self,dburl=None):
        """Load the DB URL if available
        """
        self._dburl = DB_HOST_URL if dburl == None else dburl
        if isinstance(self._dburl,bool):
            self._block = True
        else:
            self._block = False
        
        if self._block:
            return
        self._conn = psycopg2.connect(self._dburl)
        
        download_table = """
            CREATE TABLE active_downs(
                id SERIAL PRIMARY KEY NOT NULL,
                chat_id BIGINT NOT NULL,
                msg_id BIGINT NOT NULL,
                status VARCHAR(10) DEFAULT '' NOT NULL
            )
        """
        cur = self._conn.cursor()
        try:
            cur.execute("DROP TABLE active_downs")
        except:
            pass
        cur.execute(download_table)
        cur.close()
        self._conn.commit()


    def registerUpload(self,chat_id :int, msg_id :int):
        """Register a new upload that is being made, in the DB
        """
        if self._block:
            return

        sql = "INSERT INTO active_downs(chat_id,msg_id,status) VALUES(%s,%s,%s)"
        try:
            LOGGER.info("Registing the upload {} {}".format(chat_id,msg_id))
            cur = self._conn.cursor()

            cur.execute(sql,(chat_id,msg_id,'a'))

            cur.close()
            self._conn.commit()
        except Exception as e:
            LOGGER.error("Error occured while registering a Upload\n{}".format(traceback.format_exc()))

    def deregisterUpload(self,chat_id :int, msg_id :int):
        """deregister a new upload that was being made but now completed, in the DB
        """
        if self._block:
            return
        sql = "DELETE FROM active_downs WHERE chat_id=%s AND msg_id=%s"
        try:
            LOGGER.info("Deregisting the upload {} {}".format(chat_id,msg_id))
            cur = self._conn.cursor()

            cur.execute(sql,(chat_id,msg_id))

            cur.close()
            self._conn.commit()
        except Exception as e:
            LOGGER.error("Error occured while deregistering a Upload\n{}".format(traceback.format_exc()))

    def isBlocked(self,chat_id :int, msg_id :int):
        """Check if the download was bound to cancel
        """
        if self._block:
            return False
        
        sql = "SELECT * FROM active_downs WHERE chat_id=%s AND msg_id=%s AND status='can'"
        try:
            cur = self._conn.cursor()

            cur.execute(sql,(chat_id,msg_id))
            data = cur.fetchall()
            if len(data) > 0:
                return True

            cur.close()
            self._conn.commit()
        except Exception as e:
            LOGGER.error("Error occured while deregistering a Upload\n{}".format(traceback.format_exc()))
            return False
        return False

    def markCancel(self,chat_id :int, msg_id :int):
        """Mark download for cancel
        """
        if self._block:
            return False

        sql = "SELECT * FROM active_downs WHERE chat_id=%s AND msg_id=%s"
        try:
            cur = self._conn.cursor()

            cur.execute(sql,(chat_id,msg_id))
            data = cur.fetchall()
            
            if len(data) > 0:
                sql = "UPDATE active_downs SET status=%s WHERE chat_id=%s AND msg_id=%s"
                cur.execute(sql,("can",chat_id,msg_id))
                cur.close()
                self._conn.commit()
                return True
            else:
                cur.close()
                self._conn.commit()
                return False

            
        except Exception as e:
            LOGGER.error("Error occured while deregistering a Upload\n{}".format(traceback.format_exc()))
            return False
        return False
    
    def __del__(self):
        """Close connection so that the threshold is not exceeded
        """
        if self._block:
            return
        self._conn.close()