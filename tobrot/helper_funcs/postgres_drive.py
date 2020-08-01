#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
# Contributed by YashDK 

# the logging things
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
        self._dburl = DB_HOST_URL if dburl == None else dburl
        self._conn = psycopg2.connect(self._dburl)
        
        download_table = """
            CREATE TABLE IF NOT EXISTS active_downs(
                id SERIAL PRIMARY KEY NOT NULL,
                chat_id INT NOT NULL,
                msg_id INT NOT NULL,
                status VARCHAR(10) DEFAULT '' NOT NULL
            )
        """
        cur = self._conn.cursor()
        cur.execute(download_table)
        cur.close()
        self._conn.commit()


    def registerUpload(self,chat_id :int, msg_id :int):
        sql = "INSERT INTO active_downs(chat_id,msg_id,status) VALUES(%s,%s,%s)"
        try:
            LOGGER.info("Deregisting the upload {} {}".format(chat_id,msg_id))
            cur = self._conn.cursor()

            cur.execute(sql,(chat_id,msg_id,'a'))

            cur.close()
            self._conn.commit()
        except Exception as e:
            LOGGER.error("Error occured while registering a Upload\n{}".format(traceback.format_exc()))

    def deregisterUpload(self,chat_id :int, msg_id :int):
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