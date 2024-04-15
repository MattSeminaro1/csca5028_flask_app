#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, request
import psycopg2

app = Flask(__name__)

conn_params = {
    'dbname': 'db_init',
    'user': 'csca5028',
    'password': 'csca5028',
    'host': 'csca5028-db-instance.c1a04q2cyd4h.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

def get_pitchers():
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute('''SELECT distinct split_part(pitching, ' ', 1)|| ' ' || split_part(pitching, ' ', 2) as pitching
                   FROM pitching_data
                   order by split_part(pitching, ' ', 1)|| ' ' || split_part(pitching, ' ', 2)''')
    pitchers = cur.fetchall()
    cur.close()
    conn.close()
    return [pitcher[0] for pitcher in pitchers]

def get_batters():
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute('''SELECT distinct  REVERSE(SUBSTRING(REVERSE(batting), POSITION(' ' IN REVERSE(batting)) + 1)) AS batting
                    FROM batting_data''')
    batters = cur.fetchall()
    cur.close()
    conn.close()
    return [batter[0] for batter in batters]

def get_summary_statistics(player, num_games, type):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    if type == 'pitch':
        query = """
            select 'Innings Pitched' as Variable, MIN(ip) as min, AVG(ip) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ip) AS median, max(ip) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s )
                UNION ALL
                select 'Hits' as Variable, MIN(h) as min, AVG(h) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY h) AS median, max(h) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s )
                UNION ALL
                select 'Runs' as Variable, MIN(r) as min, AVG(r) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY r) AS median, max(r) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Walks' as Variable, MIN(bb) as min, AVG(bb) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bb) AS median, max(bb) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Strike Outs' as Variable, MIN(so) as min, AVG(so) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY so) AS median, max(so) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Home Runs' as Variable, MIN(hr) as min, AVG(hr) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY hr) AS median, max(hr) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Batters Faced' as Variable, MIN(bf) as min, AVG(bf) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bf) AS median, max(bf) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Pitches Thrown' as Variable, MIN(pit) as min, AVG(pit) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pit) AS median, max(pit) as max
                from (
                SELECT * 
                FROM pitching_data
                where pitching like %s
                order by upload_dttm desc
                limit %s)
                    """
        cur.execute(query, (f'%{player}%', num_games, f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games))
        summary_statistics = cur.fetchall()
    elif type == 'bat':
        query = """
            select 'At Bats' as Variable, MIN(ab) as min, AVG(ab) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ab) AS median, max(ab) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s )
                UNION ALL
                select 'Hits' as Variable, MIN(h) as min, AVG(h) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY h) AS median, max(h) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s )
                UNION ALL
                select 'Runs' as Variable, MIN(r) as min, AVG(r) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY r) AS median, max(r) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Walks' as Variable, MIN(bb) as min, AVG(bb) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bb) AS median, max(bb) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Strike Outs' as Variable, MIN(so) as min, AVG(so) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY so) AS median, max(so) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'RBI' as Variable, MIN(rbi) as min, AVG(rbi) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY rbi) AS median, max(rbi) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Batting Average' as Variable, MIN(ba) as min, AVG(ba) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ba) AS median, max(ba) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'On Base Percentage' as Variable, MIN(obp) as min, AVG(obp) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY obp) AS median, max(obp) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s)
                UNION ALL
                select 'Slugging Percentage' as Variable, MIN(slg) as min, AVG(slg) as average, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY slg) AS median, max(slg) as max
                from (
                SELECT * 
                FROM batting_data
                where batting like %s
                order by upload_dttm desc
                limit %s)
                    """
        cur.execute(query, (f'%{player}%', num_games, f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games,f'%{player}%', num_games))
        summary_statistics = cur.fetchall()

    print(summary_statistics)
    cur.close()
    conn.close()
    #print(summary_statistics)

    return summary_statistics

# Define routes and view functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select/<choice>')
def select(choice):
    if choice == 'pitching':
        return redirect(url_for('pitching'))
    elif choice == 'batting':
        return redirect(url_for('batting'))
    else:
        return "Invalid choice"


@app.route('/pitching', methods=['GET', 'POST'])  # Allow both GET and POST requests
def pitching():
    if request.method == 'POST':
        # Get pitcher and number of games from the form
        pitcher = request.form['pitcher']
        num_games = int(request.form['num_games'])

        # Get summary statistics based on the inputs
        summary_statistics = get_summary_statistics(pitcher, num_games, 'pitch')

        # Pass summary statistics to the template and render it
        return render_template('summary.html', summary_statistics=summary_statistics, player=pitcher, num_games=num_games)

    # If the request method is GET, render the form
    pitchers = get_pitchers()
    return render_template('pitching.html', pitchers=pitchers)

@app.route('/batting',  methods=['GET', 'POST'])
def batting():
    if request.method == 'POST':
        # Get pitcher and number of games from the form
        batter = request.form['batter']
        num_games = int(request.form['num_games'])

        # Get summary statistics based on the inputs
        summary_statistics = get_summary_statistics(batter, num_games, 'bat')

        # Pass summary statistics to the template and render it
        return render_template('summary.html', summary_statistics=summary_statistics, player=batter, num_games=num_games)
    batters = get_batters()
    return render_template('batting.html', batters=batters)

if __name__ == '__main__':
    app.run(debug=True)