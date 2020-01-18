# -*- coding: utf-8 -*-

#
# Copyright (c) 2012 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import redhat_support_lib.utils.confighelper as confighelper
from redhat_support_lib.web.connection import Connection
from ftplib import FTP
import base64
import tempfile
import datetime
import gzip
import logging
import os.path
import sys

logger = logging.getLogger("redhat_support_lib.utils.reporthelper")

__author__ = 'Spenser Shumaker sshumake@redhat.com'
__author__ = 'Keith Robertson kroberts@redhat.com'


def ftp_attachment(fileName=None, caseNumber=None):

    config = confighelper.get_config_helper()

    if not fileName:
        raise Exception('ftp_file(%s) cannot be empty.' % fileName)
    logger.debug("Creating connection to FTP server %s" % config.ftp_host)

    # add http to host because if it is not prefixed it defaults to https
    try:
        if config.proxy_url != None:
            conn = Connection(url="http://" + config.ftp_host,
                                         manager=None,
                                         key_file=config.key_file,
                                         cert_file=config.cert_file,
                                         timeout=config.timeout,
                                         username=config.ftp_user,
                                         password=config.ftp_pass,
                                         proxy_url=config.proxy_url,
                                         proxy_user=config.proxy_user,
                                         proxy_pass=config.proxy_pass,
                                         debug=config.http_debug)
            httpconnection = conn.getConnection()

            hdr = {'Host': config.ftp_host,
                   'Proxy-Connection': 'Keep-Alive',
                   'Accept': 'application/xml'}
            if config.proxy_user and config.proxy_pass:
                auth = base64.encodestring("%s:%s" % \
                                           (config.proxy_user,
                                            config.proxy_pass)).strip()
                hdr['Proxy-authorization'] = "Basic %s" % auth
            # Critical step.  Proxy must know where to go.
            if sys.version_info[:2] == (2, 6):
                httpconnection._set_tunnel(config.ftp_host,
                                config.ftp_port,
                                hdr)
            else:
                httpconnection.set_tunnel(config.ftp_host,
                                config.ftp_port,
                                hdr)
            httpconnection.connect()

            ftp = FTP()
            ftp.host = config.ftp_host
            ftp.sock = httpconnection.sock
            ftp.af = ftp.sock.family
            ftp.file = ftp.sock.makefile('rb')
            ftp.welcome = ftp.getresp()
            ftp.login(user=config.ftp_user, passwd=config.ftp_pass)
        else:
                ftp = FTP(host=config.ftp_host, user=config.ftp_user,
                          passwd=config.ftp_pass)
                ftp.login()
        if config.ftp_dir:
                ftp.cwd(config.ftp_dir)
        logger.debug("Sending file %s over FTP" % fileName)
        resp = ftp.storbinary('STOR ' + os.path.basename(fileName),
                              open(fileName, 'rb'))
    finally:
        if config.proxy_url != None:
            conn.close()
        else:
            ftp.close()
    return resp


def compress_attachment(fileName, caseNumber):
    file_handle = None
    tmp_dir = None
    filebaseName = os.path.basename(fileName)
    try:
        tmp_dir = tempfile.mkdtemp()
        utc_datetime = datetime.datetime.utcnow()
        gzipName = (tmp_dir + '/' + filebaseName + '.gz')
        file_handle = gzip.open(gzipName, 'w+')
        f_in = open(fileName, 'rb')
        file_handle.writelines(f_in)
    finally:
            f_in.close()
            file_handle.close()
    size = os.path.getsize(fileName)

    if size >= confighelper.get_config_helper().attachment_max_size:
        newName = tmp_dir + '/' + caseNumber + \
            utc_datetime.strftime("-%Y-%m-%d-%H%M%s-") + filebaseName + '.gz'
        os.rename(gzipName, newName)
        gzipName = newName
    return tmp_dir, gzipName
