import ConfigParser
import getpass
import urllib
import urllib2
import cookielib
import hashlib
import os
import re
import sys

class Learn:
    def __init__(self, config_file_path):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(config_file_path)
        cookie_filename = "./cookie.txt"
        self.cookie = cookielib.MozillaCookieJar(cookie_filename)
        if (os.path.exists(cookie_filename)):
            self.cookie.load(ignore_discard=True, ignore_expires=True)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [('User-Agent', self.header_user_agent)]
        self.loaded_assest = {}
        self.downloaded_file = {}
        
    @property
    def url_baseurl(self):
        return self.conf.get("url", "baseurl")
    @property
    def url_login(self):
        return self.conf.get("url", "login")
    @property
    def url_courselist(self):
        return self.conf.get("url", "courselist")
    @property
    def url_getnoteid_student(self):
        return self.conf.get("url", "getnoteid_student")
    @property
    def url_course_locate(self):
        return self.conf.get("url", "course_locate")
    @property
    def url_note_reply(self):
        return self.conf.get("url", "note_reply")
    @property
    def url_course_info(self):
        return self.conf.get("url", "course_info")
    @property
    def url_download(self):
        return self.conf.get("url", "download")
    @property
    def url_ware_list(self):
        return self.conf.get("url", "ware_list")
    @property
    def url_homework(self):
        return self.conf.get("url", "homework")
    @property
    def url_homework_detail(self):
        return self.conf.get("url", "homework_detail")
    @property
    def url_homework_view(self):
        return self.conf.get("url", "homework_view")
    @property
    def url_bbs_list(self):
        return self.conf.get("url", "bbs_list")
    @property
    def url_talk_list(self):
        return self.conf.get("url", "talk_list")
    @property
    def url_talk_reply(self):
        return self.conf.get("url", "talk_reply")
    @property
    def header_user_agent(self):
        return self.conf.get("header", "user_agent")
    @property
    def browser_default_encoding(self):
        return self.conf.get("browser", "default_encoding")
    @property
    def browser_learn_header_encoding(self):
        return self.conf.get("browser", "learn_header_encoding")
    @property
    def browser_learn_encoding(self):
        return self.conf.get("browser", "learn_encoding")
    @property
    def system_echo(self):
        return self.conf.get("system", "echo")
    @property
    def action_download_course_locate(self):
        return int(self.conf.get("action", "download_course_locate"))
    @property
    def action_download_note_list(self):
        return int(self.conf.get("action", "download_note_list"))
    @property
    def action_download_course_info(self):
        return int(self.conf.get("action", "download_course_info"))
    @property
    def action_download_download(self):
        return int(self.conf.get("action", "download_download"))
    @property
    def action_download_ware_list(self):
        return int(self.conf.get("action", "download_ware_list"))
    @property
    def action_download_homework(self):
        return int(self.conf.get("action", "download_homework"))
    @property
    def action_download_bbs_list(self):
        return int(self.conf.get("action", "download_bbs_list"))
    @property
    def action_download_talk_list(self):
        return int(self.conf.get("action", "download_talk_list"))
    @property
    def user_username(self):
        return raw_input("Username: ")
    @property
    def user_password(self):
        return getpass.getpass("Password: ")

    @staticmethod
    def filename_escape(text):
        text = re.compile(r'[\\/:\*\?"<>|].*').sub('', text)
        return '_' if text == '' else text

    def echo_success(self, text):
        if self.system_echo == 'on':
            print '[OK]', text

    def echo_failed(self, text):
        if self.system_echo == 'on':
            print '[FAILED]', text

    def relative_url_exempt(self, text, folder, home_path='.'):
        def assest_download(match):
            assest_folder = os.path.join(folder, "assest")
            if os.path.isdir(assest_folder) == False:
                os.mkdir(assest_folder)
            attr = match.group(1)
            url = match.group(3)
            hash = hashlib.sha1(url).hexdigest()
            ext = os.path.splitext(url)[1][1:]
            filename = self.filename_escape(hash if ext == '' else "%s.%s" % (hash, ext))
            if (folder not in self.loaded_assest):
                self.loaded_assest[folder] = set()
            if (hash not in self.loaded_assest[folder]):
                self.loaded_assest[folder].add(hash)
                try:
                    response = self.opener.open("%s%s" % (self.url_baseurl, url))
                    page = response.read()
                    file = open(os.path.join(assest_folder, filename), "wb")
                    file.write(page)
                    file.close()
                    self.echo_success(file.name)
                except Exception as e:
                    print e
                    self.echo_failed(os.path.join(assest_folder, filename))
            return r'%s="%s/assest/%s"' % (attr, home_path, filename)
        return re.compile(r'(href|src)=("|\')(/[^"\']+)("|\')').sub(assest_download, text)
    
    def header_decode_to_char(self, text):
        return text.decode(self.browser_learn_header_encoding)
    
    def html_decode_to_char(self, text):
        return text.decode(self.browser_learn_encoding)
        
    def char_encode_to_html(self, text):
        return text.encode(self.browser_default_encoding, 'ignore')
        
    def file_download(self, relative_url, folder): # return filename
        if (folder not in self.downloaded_file):
            self.downloaded_file[folder] = {}
        if (relative_url in self.downloaded_file[folder]):
            return self.downloaded_file[folder][relative_url]
        url = "%s%s" % (self.url_baseurl, relative_url)
        try:
            response = self.opener.open(url)
            page = response.read()
            filename = re.match(r'^attachment;filename=(.+)$', response.info().getheader('Content-Disposition')).group(1)[1: -1]
            filename = self.header_decode_to_char(filename)
            filename = self.filename_escape(filename)
            file = open(os.path.join(folder, filename), "wb")
            file.write(page)
            file.close()
            self.echo_success(file.name)
            self.downloaded_file[folder][relative_url] = filename
            return filename
        except Exception as e:
            print e
            self.echo_failed(url)
            return '404'
    
    def login(self):
        request = urllib2.Request(self.url_login)
        username = self.user_username
        password = self.user_password
        data = urllib.urlencode({"userid": username, "userpass": password})
        response = self.opener.open(request, data)
        self.cookie.save(ignore_discard=True, ignore_expires=True)
        
    def load_courselist(self):
        response = self.opener.open(self.url_courselist)
        the_page = self.html_decode_to_char(response.read())
        self.courselist = []
        for match in re.finditer(r'<a href="/MultiLanguage/lesson/student/course_locate\.jsp\?course_id=(\d*)" target="_blank">\s*(.+)\((\d+)\)\((\d{4}-\d{4}[^)]+)\)</a>', the_page):
            self.courselist.append((int(match.group(1)), match.group(2), int(match.group(3)), match.group(4)))

    def show_courselist(self):
        print 'Supported courses'
        print "%9s %-17s %s" % ("course_id", "term", "course_name")
        for course in self.courselist:
            print "%9d %13s %s" % (course[0], course[3], course[1])
            
    def download_course(self):
        course_id = int(raw_input("course_id: "))
        for course in self.courselist:
            if course[0] == course_id:
                course_name = "%s(%d)(%s)" % (course[1], course[2], course[3])
        course_name = self.filename_escape(course_name)
        print 'Download', course_name
        if os.path.isdir(course_name) == False:
            os.mkdir(course_name)
        if self.action_download_course_locate:
            self.download_course_locate(course_id, course_name)
        if self.action_download_note_list:
            self.download_note_list(course_id, course_name)
        if self.action_download_course_info:
            self.download_course_info(course_id, course_name)
        if self.action_download_download:
            self.download_download(course_id, course_name)
        if self.action_download_ware_list:
            self.download_ware_list(course_id, course_name)
        if self.action_download_homework:
            self.download_homework(course_id, course_name)
        if self.action_download_bbs_list:
            self.download_bbs_list(course_id, course_name)
        if self.action_download_talk_list:
            self.download_talk_list(course_id, course_name)

    def download_course_locate(self, course_id, folder):
        def local_file(match):
            attr = match.group(1)
            url = match.group(2)
            replace = {
                r'/MultiLanguage/public/bbs/getnoteid_student.jsp': 'note_list.html',
                r'/MultiLanguage/lesson/student/course_info.jsp': 'course_info.html',
                r'/MultiLanguage/lesson/student/download.jsp': 'download.html',
                r'/MultiLanguage/lesson/student/ware_list.jsp': 'ware_list.html',
                r'/MultiLanguage/lesson/student/hom_wk_brw.jsp': 'homework.html',
                r'/MultiLanguage/public/bbs/getbbsid_student.jsp': 'bbs_list.html',
                r'/MultiLanguage/public/bbs/gettalkid_student.jsp': 'talk_list.html',
                r'/MultiLanguage/public/discuss/main.jsp': '#',
            }
            return (r'%s=%s' % (attr, replace[url])) if url in replace else (r'%s="#"' % (attr))
        response = self.opener.open("%s?course_id=%d" % (self.url_course_locate, course_id))
        page = self.html_decode_to_char(response.read())
        page = re.compile(r'(href|src)="(/MultiLanguage/[^"\?]+)(\?[^"]+)?"').sub(local_file, page)
        file = open(os.path.join(folder, "index.html"), "w")
        file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder)))
        file.close()
        self.echo_success(file.name)

    def download_note_list(self, course_id, folder):
        def note_download(match):
            notes_folder = os.path.join(folder, 'notes')
            if os.path.isdir(notes_folder) == False:
                os.mkdir(notes_folder)
            note_id = int(match.group(2))
            url = "%s%s" % (self.url_note_reply, match.group(1))
            page = self.html_decode_to_char(self.opener.open(url).read())
            file = open(os.path.join(notes_folder, "%d.html" % (note_id)), "w")
            file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder, '..')))
            file.close()
            self.echo_success(file.name)
            return r'<a href="notes/%d.html">' % note_id
        response = self.opener.open("%s?course_id=%d" % (self.url_getnoteid_student, course_id))
        page = self.html_decode_to_char(response.read())
        page = re.compile(r'<a  href=\'note_reply\.jsp(\?bbs_type=[^i]+id=(\d+)\&course_id=(\d+))\'>').sub(note_download, page)
        file = open(os.path.join(folder, "note_list.html"), "w")
        file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder)))
        file.close()
        self.echo_success(file.name)

    def download_course_info(self, course_id, folder):
        response = self.opener.open("%s?course_id=%d" % (self.url_course_info, course_id))
        page = self.html_decode_to_char(response.read())
        file = open(os.path.join(folder, "course_info.html"), "w")
        file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder)))
        file.close()
        self.echo_success(file.name)
        
    def download_download(self, course_id, folder):
        def file_download(match):
            file_folder = os.path.join(folder, 'download')
            if os.path.isdir(file_folder) == False:
                os.mkdir(file_folder)
            file_id = int(match.group(2))
            filename = self.file_download(match.group(1), file_folder)
            return r'<a href="download/%s">' % (filename)
        response = self.opener.open("%s?course_id=%d" % (self.url_download, course_id))
        page = self.html_decode_to_char(response.read())
        page = re.compile(r'<a target="_top" href="(/uploadFile/downloadFile_student\.jsp\?module_id=322\&filePath=[^&]*&course_id=\d+\&file_id=(\d+))" >').sub(file_download, page)
        file = open(os.path.join(folder, "download.html"), "w")
        file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder)))
        file.close()
        self.echo_success(file.name)

    def download_ware_list(self, course_id, folder):
        response = self.opener.open("%s?course_id=%d" % (self.url_ware_list, course_id))
        page = self.html_decode_to_char(response.read())
        file = open(os.path.join(folder, "ware_list.html"), "w")
        file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder)))
        file.close()
        self.echo_success(file.name)
        
    def download_homework(self, course_id, folder):
        def attachment(match):
            file_folder = os.path.join(folder, 'homework', 'attachment')
            if os.path.isdir(file_folder) == False:
                os.mkdir(file_folder)
            filename = self.file_download(match.group(1), file_folder)
            return r'<a href="attachment/%s">' % (filename)
        def homework_detail(match):
            file_folder = os.path.join(folder, 'homework')
            if os.path.isdir(file_folder) == False:
                os.mkdir(file_folder)
            homework_id = int(match.group(2))
            url = "%s%s" % (self.url_homework_detail, match.group(1))
            response = self.opener.open(url)
            page = self.html_decode_to_char(response.read())
            page = re.compile(r'<a target="_top" href="(/uploadFile/downloadFile\.jsp\?[^"]+)">').sub(attachment, page)
            filename = "%d_detail.html" % (homework_id)
            file = open(os.path.join(file_folder, filename), "w")
            file.write(self.relative_url_exempt(page, folder, ".."))
            file.close()
            self.echo_success(file.name)
            return r'<a href="homework/%d_detail.html">' % (homework_id)
        def homework_view(match):
            file_folder = os.path.join(folder, 'homework')
            if os.path.isdir(file_folder) == False:
                os.mkdir(file_folder)
            homework_id = int(match.group(2))
            url = "%s%s" % (self.url_homework_view, match.group(1))
            response = self.opener.open(url)
            page = self.html_decode_to_char(response.read())
            page = re.compile(r'<a target="_top" href="(/uploadFile/downloadFile\.jsp\?[^"]+)">').sub(attachment, page)
            filename = "%d_view.html" % (homework_id)
            file = open(os.path.join(file_folder, filename), "w")
            file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder, "..")))
            file.close()
            self.echo_success(file.name)
            return 'onclick="javascript:window.location.href=\'homework/%d_view.html\'"' % (homework_id)
        response = self.opener.open("%s?course_id=%d" % (self.url_homework, course_id))
        page = self.html_decode_to_char(response.read())
        page = re.compile(r'<a href="hom_wk_detail\.jsp(\?id=(\d+)\&course_id=\d+[^"]*)">').sub(homework_detail, page)
        page = re.compile(r'onclick="javascript:window\.location\.href=\'hom_wk_view\.jsp(\?id=(\d+)\&course_id=\d+)\'"').sub(homework_view, page)
        file = open(os.path.join(folder, "homework.html"), "w")
        file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder)))
        file.close()
        self.echo_success(file.name)
        
    def download_bbs_list(self, course_id, folder):
        pass
        
    def download_talk_list(self, course_id, folder):
        def talk_download(match):
            notes_folder = os.path.join(folder, 'talks')
            if os.path.isdir(notes_folder) == False:
                os.mkdir(notes_folder)
            talk_id = int(match.group(2))
            url = "%s%s" % (self.url_talk_reply, match.group(1))
            page = self.html_decode_to_char(self.opener.open(url).read())
            page = re.compile(r'document\.location\.replace\(\'talk_list_student\.jsp\?[^\']*\'\)').sub(r'history.back(-1)', page)
            file = open(os.path.join(notes_folder, "%d.html" % (talk_id)), "w")
            file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder, '..')))
            file.close()
            self.echo_success(file.name)
            return r'<a href="talks/%d.html">' % talk_id
        response = self.opener.open("%s?course_id=%d" % (self.url_talk_list, course_id))
        page = self.html_decode_to_char(response.read())
        page = re.compile(r'<a href=\'talk_reply_student\.jsp(\?bbs_id=\d+\&course_id=\d+\&id=(\d+)[^\']*)\'>').sub(talk_download, page)
        file = open(os.path.join(folder, "talk_list.html"), "w")
        file.write(self.char_encode_to_html(self.relative_url_exempt(page, folder)))
        file.close()
        self.echo_success(file.name)


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    learn = Learn("./learn.config.ini")
    learn.load_courselist()
    if (len(learn.courselist) == 0):
        learn.login()
        learn.load_courselist()
    learn.show_courselist()
    learn.download_course()
