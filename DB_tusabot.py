import psycopg2
import psycopg2.extras

class DB_tusabot:
    
    def __init__(self, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT):
        self.DB_HOST = DB_HOST
        self.DB_NAME = DB_NAME
        self.DB_USER = DB_USER
        self.DB_PASS = DB_PASS
        self.DB_PORT = DB_PORT
         
    def get_tusapoint(self, t_id = None, author_id = None):
    
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                                
                if (t_id != None):
                    cur.execute("select * from tusapoints where id = %s;", (t_id,))
                    return cur.fetchone()
                elif (author_id != None):
                    cur.execute("select * from tusapoints where author_id = %s;", (author_id,))
                    return cur.fetchall()
                else:
                    cur.execute("select * from tusapoints")
                    return cur.fetchall()
                    
    
    def get_friend(self, friend_id=None, telegram_id=None):
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                if friend_id != None:
                    cur.execute("select * from friends where id = %s;", (friend_id,))
                elif telegram_id != None:
                    cur.execute("select * from friends where telegram_id = %s;", (telegram_id,))
                else:
                    cur.execute("select * from friends")
                    return cur.fetchall()
                    
                return cur.fetchone()
     
    def add_tusapoint(self, description = None, author_id = None):
    
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                cur.execute("insert into tusapoints (description, author_id, count_likes) values(%s,%s,%s);", (description, author_id, 0))
                return   
            
    def delete_tusapoint(self, t_id ):
    
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                cur.execute("delete from tusapoints where id = %s;", (t_id,))
                return                    
    
    def updata_tusapoint(self, t_id = None, author_id = None, count_likes = None ):
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                if author_id !=None:
                    cur.execute("UPDATE tusapoints SET author_id = %s WHERE id = %s;", (author_id, t_id))
                if count_likes !=None:
                    cur.execute("UPDATE tusapoints SET count_likes = %s WHERE id = %s;", (count_likes, t_id))
                return
    
    def like(self, author_id, t_id):
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                cur.execute("insert into likes (author_id, tusapoint_id) values(%s,%s);", (author_id, t_id))
                return
    
    def get_like(self, t_id, author_id = None):
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                if author_id == None:
                    cur.execute("select * from likes where tusapoint_id = %s;", (t_id,))
                    return cur.fetchall()
                else:
                    cur.execute("select * from likes where tusapoint_id = %s and author_id = %s;", (t_id, author_id))
                    return cur.fetchone()
                    
            
    def delete_like(self, like_id):
    
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                cur.execute("delete from likes where id = %s;", (like_id,))
                return 
    def get_admin(self, friends_id=None):
        with psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
                ) as conn:
            
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                
                if friends_id != None:
                    cur.execute("select * from admins where friends_id = %s;", (friends_id,))
                    return cur.fetchone()
                else:
                    cur.execute("select * from admins")
                    return cur.fetchall()
                    
                