# list of server information to ping
serverList = [
              {"base":"www.yourhostone.edu","file":"/index.html","port":"80"},
              {"base":"www.yourhosttwo.edu","file":"/index.html","port":"80"},
              {"base":"help.yourhost.edu","file":"/index.php","port":"443"}
            ]
            
# dictionary object for sending error email            
mail = dict(
    host = "localhost",
    subject = "Ping Down Error - ",
    to = ["pager@yourhost.edu"],
    From = "sysadmin@yourhost.edu"
)