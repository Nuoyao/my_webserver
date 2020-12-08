#!/usr/bin/env python3

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://ny2303:9414@104.196.152.219/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#

'''
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('test hopper'), ('alan turing'), ('ada lovelace');""")
'''

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args) # debug1
  
  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT * FROM stock")
  stock_name = []
  mkt_cap = []
  prof = []
  for result in cursor:
    stock_name.append(result[0])  # can also be accessed using result[0]
    mkt_cap.append(result[1])
    prof.append(result[2])
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(stock_name = stock_name, mkt_cap = mkt_cap, profile = prof)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
'''
@app.route('/another')
def another():
  return render_template("another.html")

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect(url_for('index'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
'''

@app.route('/profile/<profile_id>')
def profile(profile_id):
      print('success execute profile check at ', profile_id)

      cursor = g.conn.execute("""SELECT * FROM company_profile WHERE profile_id = """+str(profile_id)+";")
      prof = []
      for n in cursor:
          prof.append(n)
      cursor.close()

      cursor = g.conn.execute("""SELECT * FROM key_executive WHERE profile_id = """+str(profile_id)+";")
      title = []
      name = []
      pay = []
      birth = []
      for result in cursor:
          title.append(result[0])  # can also be accessed using result[0]
          name.append(result[1])
          pay.append(result[2])
          birth.append(result[3])
      cursor.close()

      context = dict(data = prof[0], title = title, name = name, pay = pay, birth = birth)

      return render_template("profile.html", **context)
      
@app.route('/historical/<stock_ticker>')
def historical(stock_ticker):
      print('success extract historical for stock_ticker at ', stock_ticker)

      cursor = g.conn.execute("""SELECT * FROM historical WHERE stock_ticker = """+"'"+str(stock_ticker)+"'"+";")
      
      # stock_ticker = []
      date = []
      adjusted_close = []
      open = []
      low = []
      high = []
      volume = []
      close = []

      for result in cursor:
            
          # stock_ticker.append(result[0])  # can also be accessed using result[0]
          date.append(result[1])
          adjusted_close.append(result[2])
          open.append(result[3])
          low.append(result[4])
          high.append(result[5])
          volume.append(result[6])
          close.append(result[7])

      stock_ticker = result[0]

      cursor.close()

      context = dict(stock_ticker = stock_ticker, date = date, adjusted_close = adjusted_close, open = open, low = low, high = high, volume = volume, close = close)

      return render_template("historical.html", **context)
      
      
@app.route('/fundamental/<stock_ticker>')
def fundamental(stock_ticker):
      print('success extract fundamental for stock_ticker at ', stock_ticker)

      cursor = g.conn.execute("""SELECT * FROM fundamental WHERE stock_ticker = """+"'"+str(stock_ticker)+"'"+";")
      
      # stock_ticker = []
      Release_Season = []
      Revenue = []
      Cost = []
      Profit = []

      for result in cursor:
            
          # stock_ticker.append(result[0])  # can also be accessed using result[0]
          Release_Season.append(result[1])
          Revenue.append(result[2])
          Cost.append(result[3])
          Profit.append(result[4])

      stock_ticker = result[0]
      cursor.close()
      context = dict(stock_ticker = stock_ticker, Release_Season = Release_Season, Revenue = Revenue, Cost = Cost, Profit = Profit)
      return render_template("fundamental.html", **context)

@app.route('/analysis')
def analysis():
    
      '''
      Analysis 1
      For each stock sector with more than one stock, we compute the sum of 
      market cap of all the stocks with positive revunue and profit in this
      sector, and also their average profit margin.
      '''
      cursor1 = g.conn.execute("""SELECT prof.sector, 
      SUM(market_cap) AS market_cap_of_sector, 
      AVG(f.profit/f.revenue) AS average_profit_margin
      FROM  (stock s JOIN company_profile prof ON s.profile_id = prof.profile_id) 
      JOIN historical h ON h.stock_ticker = s.stock_ticker
      JOIN fundamental f ON f.stock_ticker = s.stock_ticker
      WHERE f.profit > 0 AND f.revenue > 0
      GROUP BY prof.sector
      HAVING count(s.stock_ticker)>1
      ORDER BY market_cap_of_sector DESC;""")
      
      sector  = []
      cap = []
      pm = []
      
      for re in cursor1:
        sector.append(re[0])
        cap.append(round(re[1],2))
        pm.append(round(re[2],2))
        # print(re)

      cursor1.close()

      '''
      Analysis 2

      '''
      cursor2 = g.conn.execute("""WITH price_movement AS(
        SELECT 
          h.stock_ticker, h.date, h.adj_close/LAG(h.adj_close, 1) OVER (PARTITION BY stock_ticker ORDER BY h.date) AS log_change
        FROM historical h
        GROUP BY h.stock_ticker, h.date
        ORDER BY stock_ticker DESC
          )
        SELECT stock_ticker, date, MAX(log_change)-1 as maximum_percentage_increment_in_a_month
        FROM price_movement 
        WHERE log_change in (SELECT MAX(log_change) FROM price_movement GROUP BY stock_ticker) 
        AND date Between '2020-10-1' AND '2020-10-31'
        GROUP BY stock_ticker, date
        ORDER BY stock_ticker ASC;
        """
        )
      
      stock = []
      date = []
      increment = []
      
      for re in cursor2:
        stock.append(re[0])
        date.append(re[1])
        increment.append(round(re[2]*100,3))
        # print(re)

      cursor2.close()

      context = dict(sector = sector, cap = cap, pm = pm, stock = stock, date = date, increment = increment)
      return render_template("analysis.html", **context)

# 运行主程序！
if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
