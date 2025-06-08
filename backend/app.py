from flask import Flask, request, jsonify, send_from_directory, g, render_template, redirect, url_for, flash, session,send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime, timedelta
import uuid
import json
import atexit
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DATABASE'] = 'faculty.db'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads'

jwt = JWTManager(app)
CORS(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database helper functions
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db_1(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def close_db(error):
    close_db_1(error)
def init_ww2_data():
    """Initialize WW2 map data"""
    db = get_db()
    cursor = db.cursor()
    
    # Create tables for WW2 data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ww2_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            event_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ww2_frontlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            front_name TEXT NOT NULL,
            coordinates TEXT NOT NULL,
            theater TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert comprehensive WW2 events
    sample_events = [
        # 1939 Events
        ('1939-09-01', 'Invasion of Poland', 'Germany invades Poland, starting WW2', 52.2297, 21.0122, 'invasion'),
        ('1939-09-17', 'Soviet invasion of Poland', 'USSR invades Poland from the east', 52.0975, 23.7340, 'invasion'),
        ('1939-11-30', 'Winter War begins', 'USSR attacks Finland', 60.1699, 24.9384, 'invasion'),
        
        # 1940 Events
        ('1940-04-09', 'Operation Weserübung', 'Germany invades Denmark and Norway', 59.9139, 10.7522, 'invasion'),
        ('1940-05-10', 'Battle of France begins', 'Germany invades France, Belgium, Netherlands', 50.8503, 4.3517, 'invasion'),
        ('1940-05-26', 'Dunkirk Evacuation', 'Allied evacuation from Dunkirk', 51.0344, 2.3768, 'evacuation'),
        ('1940-06-22', 'Fall of France', 'France surrenders to Germany', 48.8566, 2.3522, 'surrender'),
        ('1940-07-10', 'Battle of Britain begins', 'German air campaign against Britain', 51.5074, -0.1278, 'battle'),
        ('1940-09-27', 'Tripartite Pact', 'Germany, Italy, Japan form alliance', 35.6762, 139.6503, 'alliance'),
        
        # 1941 Events
        ('1941-04-06', 'Invasion of Yugoslavia', 'Axis powers invade Yugoslavia', 44.7866, 20.4489, 'invasion'),
        ('1941-04-06', 'Battle of Greece', 'Germany invades Greece', 37.9838, 23.7275, 'invasion'),
        ('1941-05-20', 'Battle of Crete', 'German airborne invasion of Crete', 35.2401, 24.8093, 'battle'),
        ('1941-06-22', 'Operation Barbarossa', 'Germany invades Soviet Union', 55.7558, 37.6176, 'invasion'),
        ('1941-07-09', 'Siege of Leningrad begins', 'German forces begin siege of Leningrad', 59.9311, 30.3609, 'siege'),
        ('1941-08-25', 'Anglo-Soviet invasion of Iran', 'Britain and USSR invade Iran', 35.6892, 51.3890, 'invasion'),
        ('1941-09-08', 'Siege of Leningrad tightens', 'City completely surrounded', 59.9311, 30.3609, 'siege'),
        ('1941-09-30', 'Operation Typhoon', 'German offensive towards Moscow', 55.7558, 37.6176, 'offensive'),
        ('1941-10-02', 'Battle of Moscow begins', 'German forces approach Moscow', 55.7558, 37.6176, 'battle'),
        ('1941-12-06', 'Soviet Winter Offensive', 'Red Army counter-attacks at Moscow', 55.7558, 37.6176, 'offensive'),
        ('1941-12-07', 'Pearl Harbor', 'Japanese attack on Pearl Harbor', 21.3099, -157.8581, 'attack'),
        
        # 1942 Events
        ('1942-01-20', 'Wannsee Conference', 'Nazi planning of Holocaust', 52.5200, 13.4050, 'conference'),
        ('1942-04-18', 'Doolittle Raid', 'First US air raid on Japanese mainland', 35.6762, 139.6503, 'raid'),
        ('1942-05-08', 'Battle of the Coral Sea', 'First major naval battle in Pacific', -15.0000, 155.0000, 'battle'),
        ('1942-05-12', 'Second Battle of Kharkov', 'Failed Soviet offensive', 49.9935, 36.2304, 'battle'),
        ('1942-06-04', 'Battle of Midway', 'Decisive US naval victory', 28.2072, -177.3735, 'battle'),
        ('1942-06-28', 'Operation Blue begins', 'German summer offensive in USSR', 48.7080, 44.5133, 'offensive'),
        ('1942-07-17', 'Battle of Stalingrad begins', 'German forces reach Stalingrad', 48.7080, 44.5133, 'battle'),
        ('1942-08-07', 'Guadalcanal Campaign', 'First major Allied ground offensive', -9.4280, 159.9540, 'campaign'),
        ('1942-08-23', 'Battle of Stalingrad intensifies', 'Major turning point on Eastern Front', 48.7080, 44.5133, 'battle'),
        ('1942-10-23', 'Second Battle of El Alamein', 'British victory in North Africa', 30.8333, 28.9667, 'battle'),
        ('1942-11-08', 'Operation Torch', 'Allied invasion of North Africa', 36.7538, -3.0588, 'invasion'),
        ('1942-11-19', 'Operation Uranus', 'Soviet counter-offensive at Stalingrad', 48.7080, 44.5133, 'offensive'),
        
        # 1943 Events
        ('1943-01-14', 'Casablanca Conference', 'Allied strategic planning', 33.5731, -7.5898, 'conference'),
        ('1943-01-18', 'Siege of Leningrad broken', 'Soviet forces break siege', 59.9311, 30.3609, 'victory'),
        ('1943-02-02', 'Stalingrad victory', 'Soviet victory at Stalingrad', 48.7080, 44.5133, 'victory'),
        ('1943-03-15', 'Third Battle of Kharkov', 'German recapture of Kharkov', 49.9935, 36.2304, 'battle'),
        ('1943-04-19', 'Warsaw Ghetto Uprising', 'Jewish resistance in Warsaw', 52.2297, 21.0122, 'uprising'),
        ('1943-05-13', 'Tunisia Campaign ends', 'Axis forces surrender in North Africa', 36.8065, 10.1815, 'victory'),
        ('1943-07-05', 'Battle of Kursk', 'Largest tank battle in history', 51.7373, 36.1873, 'battle'),
        ('1943-07-09', 'Allied invasion of Sicily', 'Operation Husky begins', 37.5079, 15.0830, 'invasion'),
        ('1943-07-25', 'Fall of Mussolini', 'Italian dictator removed from power', 41.9028, 12.4964, 'political'),
        ('1943-08-23', 'Battle of Kursk ends', 'Soviet victory, German retreat', 51.7373, 36.1873, 'victory'),
        ('1943-09-03', 'Allied invasion of Italy', 'Italy invaded from Sicily', 38.1157, 15.6516, 'invasion'),
        ('1943-09-08', 'Italy surrenders', 'Italian government surrenders to Allies', 41.9028, 12.4964, 'surrender'),
        ('1943-11-06', 'Kiev liberated', 'Soviet forces recapture Kiev', 50.4501, 30.5234, 'liberation'),
        
        # 1944 Events
        ('1944-01-27', 'Siege of Leningrad ends', 'Complete lifting of the siege', 59.9311, 30.3609, 'liberation'),
        ('1944-03-19', 'German occupation of Hungary', 'Germany occupies Hungary', 47.4979, 19.0402, 'occupation'),
        ('1944-04-10', 'Odessa liberated', 'Soviet forces recapture Odessa', 46.4825, 30.7233, 'liberation'),
        ('1944-05-09', 'Sevastopol liberated', 'Soviet forces recapture Sevastopol', 44.6160, 33.5254, 'liberation'),
        ('1944-06-04', 'Rome liberated', 'Allied forces enter Rome', 41.9028, 12.4964, 'liberation'),
        ('1944-06-06', 'D-Day', 'Allied invasion of Normandy', 49.3967, -0.4431, 'invasion'),
        ('1944-06-15', 'Battle of Saipan', 'Strategic island captured by US', 15.1979, 145.7394, 'battle'),
        ('1944-06-23', 'Operation Bagration', 'Massive Soviet offensive in Belarus', 53.9006, 27.5590, 'offensive'),
        ('1944-07-03', 'Minsk liberated', 'Soviet forces recapture Minsk', 53.9006, 27.5590, 'liberation'),
        ('1944-07-20', 'July 20 Plot', 'Failed assassination attempt on Hitler', 54.0924, 12.2989, 'assassination'),
        ('1944-08-01', 'Warsaw Uprising', 'Polish resistance uprising', 52.2297, 21.0122, 'uprising'),
        ('1944-08-20', 'Operation Dragoon', 'Allied invasion of Southern France', 43.2965, 5.3698, 'invasion'),
        ('1944-08-23', 'Romania switches sides', 'Romania joins Allies', 44.4268, 26.1025, 'political'),
        ('1944-08-25', 'Liberation of Paris', 'Allied forces liberate Paris', 48.8566, 2.3522, 'liberation'),
        ('1944-09-08', 'Bulgaria switches sides', 'Bulgaria joins Allies', 42.6977, 23.3219, 'political'),
        ('1944-09-17', 'Operation Market Garden', 'Failed Allied airborne operation', 51.9851, 5.8987, 'operation'),
        ('1944-10-14', 'Riga liberated', 'Soviet forces recapture Riga', 56.9496, 24.1052, 'liberation'),
        ('1944-10-20', 'Philippines Campaign', 'MacArthur returns to Philippines', 11.0000, 125.0000, 'campaign'),
        ('1944-10-20', 'Belgrade liberated', 'Soviet and Yugoslav forces take Belgrade', 44.7866, 20.4489, 'liberation'),
        ('1944-11-24', 'B-29 raids on Japan', 'Strategic bombing of Japan begins', 35.6762, 139.6503, 'bombing'),
        ('1944-12-16', 'Battle of the Bulge', 'German counter-offensive in Ardennes', 50.0755, 5.7682, 'battle'),
        
        # 1945 Events
        ('1945-01-12', 'Vistula-Oder Offensive', 'Massive Soviet offensive in Poland', 52.2297, 21.0122, 'offensive'),
        ('1945-01-17', 'Warsaw liberated', 'Soviet forces liberate Warsaw', 52.2297, 21.0122, 'liberation'),
        ('1945-01-27', 'Auschwitz liberated', 'Soviet forces liberate Auschwitz', 50.0347, 19.2041, 'liberation'),
        ('1945-02-04', 'Yalta Conference', 'Allied leaders meet at Yalta', 44.4952, 34.1742, 'conference'),
        ('1945-02-13', 'Bombing of Dresden', 'Allied bombing of Dresden', 51.0504, 13.7373, 'bombing'),
        ('1945-02-19', 'Battle of Iwo Jima', 'Costly US victory', 24.7854, 141.3128, 'battle'),
        ('1945-03-07', 'Remagen Bridge', 'Allies cross Rhine at Remagen', 50.5791, 7.2461, 'crossing'),
        ('1945-04-01', 'Battle of Okinawa', 'Last major Pacific battle', 26.2540, 127.6990, 'battle'),
        ('1945-04-12', 'Death of Roosevelt', 'US President Roosevelt dies', 32.8407, -84.2557, 'death'),
        ('1945-04-16', 'Battle of Berlin begins', 'Soviet assault on Berlin', 52.5200, 13.4050, 'battle'),
        ('1945-04-25', 'Elbe Day', 'US and Soviet forces meet at Elbe', 51.8661, 12.6950, 'meeting'),
        ('1945-04-28', 'Mussolini executed', 'Italian dictator executed', 45.8205, 9.1584, 'execution'),
        ('1945-04-30', 'Hitler suicide', 'Hitler commits suicide in Berlin bunker', 52.5200, 13.4050, 'suicide'),
        ('1945-05-02', 'Fall of Berlin', 'Soviet forces capture Berlin', 52.5200, 13.4050, 'victory'),
        ('1945-05-08', 'VE Day', 'Victory in Europe', 52.5200, 13.4050, 'victory'),
        ('1945-08-06', 'Hiroshima', 'First atomic bomb dropped', 34.3853, 132.4553, 'bombing'),
        ('1945-08-08', 'Soviet invasion of Manchuria', 'USSR enters war against Japan', 43.8171, 125.3238, 'invasion'),
        ('1945-08-09', 'Nagasaki', 'Second atomic bomb dropped', 32.7503, 129.8779, 'bombing'),
        ('1945-08-15', 'VJ Day', 'Victory over Japan', 35.6762, 139.6503, 'victory'),
        ('1945-09-02', 'Japanese surrender', 'Formal surrender ceremony', 35.6762, 139.6503, 'surrender')
    ]
    
    cursor.executemany('''        INSERT OR IGNORE INTO ww2_events (date, title, description, latitude, longitude, event_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_events)
    
    # Insert detailed front lines with more points (Eastern Front)
    eastern_front_lines = [
        # Operation Barbarossa - Initial German advance (June 22, 1941)
        ('1941-06-22', 'Eastern Front - Operation Barbarossa Start', json.dumps([
            [69.7, 33.0],   # Murmansk front
            [68.5, 33.1],   # Pechenga
            [67.9, 32.9],   # Kirkenes area
            [66.5, 25.7],   # Rovaniemi area
            [65.0, 25.5],   # Arctic Circle
            [64.5, 40.5],   # Arkhangelsk area
            [63.7, 38.3],   # Kotlas area
            [62.0, 34.3],   # Petrozavodsk area
            [61.8, 34.4],   # Lake Onega
            [60.7, 28.7],   # Vyborg area
            [59.9, 30.3],   # Leningrad
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod
            [57.8, 28.4],   # Pskov
            [57.0, 39.4],   # Yaroslavl area
            [56.8, 35.9],   # Velikiye Luki
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.2, 36.6],   # Kaluga area
            [54.5, 36.3],   # Tula area
            [53.2, 34.4],   # Bryansk
            [52.6, 32.0],   # Kursk area
            [51.7, 36.2],   # Belgorod area
            [50.4, 30.5],   # Kiev
            [49.6, 36.2],   # Poltava
            [49.0, 31.4],   # Cherkasy
            [48.5, 35.1],   # Dnipro
            [47.9, 35.1],   # Melitopol
            [47.1, 39.4],   # Rostov-on-Don
            [46.3, 30.7],   # Odessa
            [45.3, 28.6],   # Moldavia
            [45.0, 28.0]    # Danube Delta
        ]), 'Eastern'),
        
        # German advance - August 1941
        ('1941-08-15', 'Eastern Front - German Summer Advance', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish advance)
            [61.8, 34.4],   # Lake Onega (Finnish advance)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [59.9, 30.3],   # Leningrad (approaching siege)
            [59.5, 30.1],   # Leningrad suburbs
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod (German advance)
            [58.0, 32.0],   # Tikhvin area
            [57.8, 28.4],   # Pskov (German control)
            [57.0, 39.4],   # Yaroslavl area
            [56.8, 35.9],   # Velikiye Luki (German advance)
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area (approaching)
            [55.5, 38.5],   # Closer to Moscow
            [55.2, 36.6],   # Kaluga area (German advance)
            [54.5, 36.3],   # Tula area (approaching)
            [54.2, 37.6],   # South of Moscow
            [53.2, 34.4],   # Bryansk (German control)
            [52.6, 39.6],   # Voronezh area
            [51.7, 36.2],   # Belgorod area
            [50.9, 39.0],   # Lugansk area
            [50.4, 30.5],   # Kiev (under siege)
            [49.6, 36.2],   # Poltava (German advance)
            [49.0, 31.4],   # Cherkasy (German advance)
            [48.7, 44.5],   # Stalingrad area (approaching)
            [48.5, 35.1],   # Dnipro (German advance)
            [47.9, 35.1],   # Melitopol (German control)
            [47.1, 39.4],   # Rostov-on-Don (approaching)
            [46.3, 30.7],   # Odessa (under siege)
            [45.3, 28.6],   # Moldavia (German/Romanian control)
            [45.0, 37.0]    # Kuban area (approaching)
        ]), 'Eastern'),
        
        # Maximum German advance - November 1941
        ('1941-11-15', 'Eastern Front - Maximum German Advance 1941', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish control)
            [61.8, 34.4],   # Lake Onega (Finnish control)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [59.9, 30.3],   # Leningrad (besieged)
            [59.5, 30.1],   # Leningrad suburbs (German control)
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod (German control)
            [58.0, 32.0],   # Tikhvin (German control)
            [57.8, 28.4],   # Pskov (German control)
            [57.0, 39.4],   # Yaroslavl area
            [56.8, 35.9],   # Velikiye Luki (German control)
            [56.3, 43.9],   # Nizhny Novgorod area
            [56.0, 40.0],   # Gorky area (closest approach)
            [55.8, 37.6],   # Moscow area
            [55.0, 38.5],   # Closest approach to Moscow
            [54.8, 37.8],   # Moscow suburbs (closest point)
            [54.5, 36.3],   # Tula area (German advance)
            [54.2, 37.6],   # South of Moscow (German advance)
            [53.2, 34.4],   # Bryansk (German control)
            [52.6, 39.6],   # Voronezh area
            [51.7, 36.2],   # Belgorod area
            [51.5, 39.2],   # Voronezh (approaching)
            [50.9, 39.0],   # Lugansk area
            [50.4, 30.5],   # Kiev (German control)
            [49.6, 36.2],   # Poltava (German control)
            [49.0, 31.4],   # Cherkasy (German control)
            [48.7, 44.5],   # Stalingrad area (approaching)
            [48.5, 35.1],   # Dnipro (German control)
            [47.9, 35.1],   # Melitopol (German control)
            [47.1, 39.4],   # Rostov-on-Don (briefly captured)
            [46.8, 40.1],   # Taganrog area
            [46.3, 30.7],   # Odessa (German control)
            [45.3, 28.6],   # Moldavia (Axis control)
            [45.3, 36.6],   # Maikop area (approaching)
            [45.0, 37.0]    # Kuban area
        ]), 'Eastern'),
        
        # After Moscow counter-offensive - January 1942
        ('1942-01-15', 'Eastern Front - After Moscow Counter-offensive', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish control)
            [61.8, 34.4],   # Lake Onega (Finnish control)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [59.9, 30.3],   # Leningrad (still besieged)
            [59.5, 30.1],   # Leningrad suburbs (German control)
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod (German control)
            [58.0, 32.0],   # Tikhvin (recaptured by Soviets)
            [57.8, 28.4],   # Pskov (German control)
            [57.0, 39.4],   # Yaroslavl area
            [57.0, 34.0],   # Demyansk pocket
            [56.8, 35.9],   # Velikiye Luki area
            [56.5, 36.0],   # Rzhev salient
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area (Germans pushed back)
            [55.5, 36.5],   # Moscow area (Soviet control)
            [55.2, 36.6],   # Kaluga area (recaptured)
            [54.5, 36.3],   # Tula area (Soviet control)
            [54.2, 37.6],   # South of Moscow (Soviet control)
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.6, 39.6],   # Voronezh area
            [51.7, 39.2],   # Belgorod area
            [51.5, 39.2],   # Voronezh
            [50.9, 39.0],   # Lugansk area
            [50.4, 30.5],   # Kiev area
            [49.6, 36.2],   # Poltava area
            [49.0, 31.4],   # Cherkasy area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.0],   # Dnipro area
            [47.8, 35.1],   # Melitopol area
            [47.1, 39.4],   # Rostov-on-Don (recaptured by Soviets)
            [46.8, 40.1],   # Taganrog area
            [46.3, 30.7],   # Odessa area
            [45.3, 28.6],   # Moldavia
            [45.0, 37.0]    # Kuban area
        ]), 'Eastern'),
        
        # Case Blue - German summer offensive 1942
        ('1942-08-01', 'Eastern Front - Case Blue Offensive', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish control)
            [61.8, 34.4],   # Lake Onega (Finnish control)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [59.9, 30.3],   # Leningrad (still besieged)
            [59.5, 30.1],   # Leningrad suburbs
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod area
            [58.0, 32.0],   # Tikhvin area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [57.0, 34.0],   # Demyansk area
            [56.8, 35.9],   # Velikiye Luki area
            [56.5, 36.0],   # Rzhev salient
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow defensive line
            [54.5, 36.3],   # Tula area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
                        [52.6, 39.6],   # Voronezh area
            [51.5, 36.2],   # Kursk
            [50.6, 36.6],   # Kharkov (recaptured by Germans)
            [50.4, 30.5],   # Kiev area
            [49.6, 36.2],   # Poltava area
            [49.2, 40.1],   # Donetsk area
            [48.7, 44.5],   # Stalingrad (battle begins)
            [48.5, 35.1],   # Dnipro area
            [47.8, 35.1],   # Melitopol area
            [47.1, 39.4],   # Rostov-on-Don (recaptured by Germans)
            [46.8, 40.1],   # Taganrog area
            [46.3, 48.0],   # Astrakhan area (approaching)
            [45.3, 28.6],   # Moldavia
            [44.0, 43.0],   # Caucasus - Grozny area
            [43.6, 39.7],   # Sochi area (furthest south)
            [43.3, 44.7],   # Grozny area
            [44.0, 40.0]    # Caucasus mountains
        ]), 'Eastern'),
        
        # Stalingrad battle peak - November 1942
        ('1942-11-01', 'Eastern Front - Stalingrad Battle Peak', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish control)
            [61.8, 34.4],   # Lake Onega (Finnish control)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [59.9, 30.3],   # Leningrad (siege continues)
            [59.5, 30.1],   # Leningrad suburbs
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod area
            [58.0, 32.0],   # Tikhvin area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [57.0, 34.0],   # Demyansk area
            [56.8, 35.9],   # Velikiye Luki area
            [56.5, 36.0],   # Rzhev salient
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.5, 36.3],   # Tula area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.6, 39.6],   # Voronezh area
            [51.5, 36.2],   # Kursk
            [50.6, 36.6],   # Kharkov
            [50.4, 30.5],   # Kiev area
            [49.6, 36.2],   # Poltava area
            [49.2, 40.1],   # Donetsk area
            [48.7, 44.5],   # Stalingrad (fierce fighting)
            [48.6, 44.4],   # Stalingrad suburbs
            [48.5, 35.1],   # Dnipro area
            [47.8, 35.1],   # Melitopol area
            [47.1, 39.4],   # Rostov-on-Don
            [46.8, 40.1],   # Taganrog area
            [46.5, 48.0],   # Astrakhan approach
            [45.3, 28.6],   # Moldavia
            [44.0, 43.0],   # Caucasus - Grozny area
            [43.6, 39.7],   # Sochi area
            [43.3, 44.7],   # Grozny area
            [44.0, 40.0]    # Caucasus mountains
        ]), 'Eastern'),
        
        # After Stalingrad - March 1943
        ('1943-03-01', 'Eastern Front - After Stalingrad', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish control)
            [61.8, 34.4],   # Lake Onega (Finnish control)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [59.9, 30.3],   # Leningrad (siege broken)
            [59.5, 30.1],   # Leningrad suburbs (Soviet control)
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod area
            [58.0, 32.0],   # Tikhvin area
            [57.8, 28.4],   # Pskov area
            [57.5, 31.0],   # Demyansk evacuated
            [57.0, 39.4],   # Yaroslavl area
            [56.8, 35.9],   # Velikiye Luki area
            [56.0, 35.5],   # Rzhev evacuated
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.5, 36.3],   # Tula area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.6, 39.6],   # Voronezh area
            [51.5, 36.2],   # Kursk salient
            [50.6, 36.6],   # Kharkov (retaken by Germans)
            [50.4, 30.5],   # Kiev area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area (Soviet control)
            [48.5, 35.1],   # Dnipro area
            [47.5, 35.0],   # Zaporizhzhia area
            [47.1, 39.4],   # Rostov-on-Don area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa area
            [46.0, 30.0],   # Southern Ukraine
            [45.3, 28.6]    # Moldavia
        ]), 'Eastern'),
        
        # After Kursk - August 1943
        ('1943-08-15', 'Eastern Front - After Kursk Battle', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish control)
            [61.8, 34.4],   # Lake Onega (Finnish control)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [60.0, 30.3],   # Leningrad area
            [59.5, 30.1],   # Leningrad suburbs
            [59.2, 39.9],   # Vologda area
            [58.5, 31.3],   # Novgorod area
            [58.0, 31.5],   # Novgorod area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [56.8, 35.9],   # Velikiye Luki area
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.5, 36.3],   # Tula area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.5, 36.0],   # Kursk (Soviet victory)
            [52.0, 39.0],   # Voronezh area
            [51.5, 36.2],   # Belgorod area
            [50.0, 36.6],   # Kharkov (retaken by Soviets)
            [50.4, 30.5],   # Kiev area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.1],   # Dnipro line
            [47.8, 35.1],   # Melitopol area
            [47.1, 39.4],   # Rostov area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa area
            [46.0, 30.0],   # Southern Ukraine
            [45.3, 28.6]    # Moldavia
        ]), 'Eastern'),
        
        # Soviet winter offensive 1943-44
        ('1944-01-01', 'Eastern Front - Soviet Winter Offensive 1944', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk (Finnish control)
            [61.8, 34.4],   # Lake Onega (Finnish control)
            [60.7, 28.7],   # Vyborg (Finnish control)
            [60.0, 30.3],   # Leningrad (siege fully lifted)
            [59.5, 30.1],   # Leningrad suburbs
            [59.2, 39.9],   # Vologda area
            [58.5, 27.0],   # Estonia area
            [58.0, 31.5],   # Novgorod area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [56.9, 24.1],   # Latvia area
            [56.8, 35.9],   # Velikiye Luki area
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.7, 25.3],   # Lithuania area
            [54.5, 36.3],   # Tula area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.5, 36.0],   # Kursk area
            [52.2, 21.0],   # Poland border
            [52.0, 39.0],   # Voronezh area
            [51.5, 36.2],   # Belgorod area
            [50.4, 30.5],   # Kiev (liberated)
            [50.0, 36.6],   # Kharkov area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.1],   # Dnipro area
            [47.8, 35.1],   # Melitopol (liberated)
            [47.1, 39.4],   # Rostov area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa area
            [46.0, 30.0],   # Southern Ukraine
            [45.3, 28.6]    # Moldavia
        ]), 'Eastern'),
        
        # Operation Bagration - July 1944
        ('1944-07-01', 'Eastern Front - Operation Bagration', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk area
                        [61.8, 34.4],   # Lake Onega area
            [60.7, 28.7],   # Vyborg area
            [60.0, 30.3],   # Leningrad area
            [59.4, 24.8],   # Estonia (Soviet advance)
            [59.2, 39.9],   # Vologda area
            [58.5, 27.0],   # Estonia area
            [58.0, 31.5],   # Novgorod area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [56.9, 24.1],   # Latvia (Soviet advance)
            [56.8, 35.9],   # Velikiye Luki area
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.7, 25.3],   # Lithuania (Soviet advance)
            [54.5, 36.3],   # Tula area
            [54.0, 23.0],   # East Prussia border
            [53.9, 27.6],   # Minsk (liberated)
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.5, 36.0],   # Kursk area
            [52.2, 21.0],   # Warsaw area
            [52.0, 39.0],   # Voronezh area
            [51.5, 36.2],   # Belgorod area
            [51.0, 17.0],   # Wroclaw area
            [50.4, 30.5],   # Kiev area
            [50.0, 36.6],   # Kharkov area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.1],   # Dnipro area
            [47.8, 35.1],   # Melitopol area
            [47.1, 39.4],   # Rostov area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa (liberated)
            [46.0, 30.0],   # Southern Ukraine
            [45.3, 28.6],   # Moldavia
            [44.4, 26.1]    # Romania border
        ]), 'Eastern'),
        
        # Autumn 1944 - Soviet advance into Balkans
        ('1944-10-01', 'Eastern Front - Advance into Balkans', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk area
            [61.8, 34.4],   # Lake Onega area
            [60.7, 28.7],   # Vyborg area
            [60.0, 30.3],   # Leningrad area
            [59.4, 24.8],   # Estonia (liberated)
            [59.2, 39.9],   # Vologda area
            [58.5, 27.0],   # Estonia area
            [58.0, 31.5],   # Novgorod area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [56.9, 24.1],   # Latvia (liberated)
            [56.8, 35.9],   # Velikiye Luki area
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.7, 25.3],   # Lithuania (liberated)
            [54.5, 36.3],   # Tula area
            [54.0, 23.0],   # East Prussia border
            [53.9, 27.6],   # Minsk area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.5, 36.0],   # Kursk area
            [52.2, 21.0],   # Warsaw area
            [52.0, 39.0],   # Voronezh area
            [51.5, 36.2],   # Belgorod area
            [51.0, 17.0],   # Wroclaw area
            [50.4, 30.5],   # Kiev area
            [50.0, 36.6],   # Kharkov area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.1],   # Dnipro area
            [47.8, 35.1],   # Melitopol area
            [47.5, 19.0],   # Budapest area
            [47.1, 39.4],   # Rostov area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa area
            [46.0, 30.0],   # Southern Ukraine
            [45.3, 28.6],   # Moldavia
            [44.8, 20.4],   # Belgrade (liberated)
            [44.4, 26.1],   # Romania (switched sides)
            [43.2, 27.9],   # Bulgaria area
            [42.7, 23.3]    # Sofia area
        ]), 'Eastern'),
        
        # Vistula-Oder Offensive - January 1945
        ('1945-01-15', 'Eastern Front - Vistula-Oder Offensive', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk area
            [61.8, 34.4],   # Lake Onega area
            [60.7, 28.7],   # Vyborg area
            [60.0, 30.3],   # Leningrad area
            [59.4, 24.8],   # Estonia
            [59.2, 39.9],   # Vologda area
            [58.5, 27.0],   # Estonia area
            [58.0, 31.5],   # Novgorod area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [56.9, 24.1],   # Latvia
            [56.8, 35.9],   # Velikiye Luki area
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.7, 25.3],   # Lithuania
            [54.5, 36.3],   # Tula area
            [54.0, 20.0],   # Gdansk area
            [53.9, 27.6],   # Minsk area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.5, 36.0],   # Kursk area
            [52.2, 21.0],   # Warsaw (liberated)
            [52.0, 39.0],   # Voronezh area
            [51.5, 36.2],   # Belgorod area
            [51.1, 17.0],   # Wroclaw area
            [50.8, 14.4],   # Dresden area
            [50.4, 30.5],   # Kiev area
            [50.0, 36.6],   # Kharkov area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.1],   # Dnipro area
            [47.8, 35.1],   # Melitopol area
            [47.5, 19.0],   # Budapest (under siege)
            [47.1, 39.4],   # Rostov area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa area
            [46.0, 30.0],   # Southern Ukraine
            [45.3, 28.6],   # Moldavia
            [44.8, 20.4],   # Belgrade area
            [44.4, 26.1],   # Romania
            [43.2, 27.9],   # Bulgaria area
            [42.7, 23.3]    # Sofia area
        ]), 'Eastern'),
        
        # Final assault on Berlin - April 1945
        ('1945-04-15', 'Eastern Front - Final Assault on Berlin', json.dumps([
            [69.7, 33.0],   # Murmansk (unchanged)
            [68.5, 33.1],   # Pechenga (unchanged)
            [67.9, 32.9],   # Kirkenes area (unchanged)
            [66.5, 25.7],   # Rovaniemi area (unchanged)
            [65.0, 25.5],   # Arctic Circle (unchanged)
            [64.5, 40.5],   # Arkhangelsk (unchanged)
            [63.7, 38.3],   # Kotlas area (unchanged)
            [62.0, 34.3],   # Petrozavodsk area
            [61.8, 34.4],   # Lake Onega area
            [60.7, 28.7],   # Vyborg area
            [60.0, 30.3],   # Leningrad area
            [59.4, 24.8],   # Estonia
            [59.2, 39.9],   # Vologda area
            [58.5, 27.0],   # Estonia area
            [58.0, 31.5],   # Novgorod area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [56.9, 24.1],   # Latvia
            [56.8, 35.9],   # Velikiye Luki area
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.7, 25.3],   # Lithuania
            [54.5, 36.3],   # Tula area
            [54.3, 13.4],   # Berlin suburbs
            [54.0, 20.0],   # Gdansk area
            [53.9, 27.6],   # Minsk area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.5, 13.4],   # Berlin (under assault)
            [52.2, 21.0],   # Warsaw area
            [52.0, 39.0],   # Voronezh area
            [51.5, 36.2],   # Belgorod area
            [51.1, 17.0],   # Wroclaw area
            [50.8, 14.4],   # Dresden area
            [50.4, 30.5],   # Kiev area
            [50.1, 14.4],   # Prague area
            [50.0, 36.6],   # Kharkov area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.1],   # Dnipro area
            [48.2, 16.4],   # Vienna (captured)
            [47.8, 35.1],   # Melitopol area
            [47.5, 19.0],   # Budapest (liberated)
            [47.1, 39.4],   # Rostov area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa area
            [46.1, 14.8],   # Ljubljana area
            [46.0, 30.0],   # Southern Ukraine
            [45.3, 28.6],   # Moldavia
            [44.8, 20.4],   # Belgrade area
            [44.4, 26.1],   # Romania
            [43.2, 27.9],   # Bulgaria area
            [42.7, 23.3]    # Sofia area
        ]), 'Eastern'),
        
        # Victory in Europe - May 8, 1945
        ('1945-05-08', 'Eastern Front - Victory in Europe', json.dumps([
            [69.7, 33.0],   # Murmansk
            [68.5, 33.1],   # Pechenga
            [67.9, 32.9],   # Kirkenes area
            [66.5, 25.7],   # Rovaniemi area
            [65.0, 25.5],   # Arctic Circle
            [64.5, 40.5],   # Arkhangelsk
            [63.7, 38.3],   # Kotlas area
            [62.6, 29.8],   # Petrozavodsk area
            [61.8, 34.4],   # Lake Onega area
            [60.7, 28.7],   # Vyborg area
            [60.0, 30.3],   # Leningrad area
                        [59.4, 24.8],   # Estonia
            [59.2, 39.9],   # Vologda area
            [58.5, 27.0],   # Estonia area
            [58.0, 31.5],   # Novgorod area
            [57.8, 28.4],   # Pskov area
            [57.0, 39.4],   # Yaroslavl area
            [56.9, 24.1],   # Latvia
            [56.8, 35.9],   # Velikiye Luki area
            [56.3, 43.9],   # Nizhny Novgorod area
            [55.8, 37.6],   # Moscow area
            [55.0, 36.0],   # Moscow area
            [54.7, 25.3],   # Lithuania
            [54.5, 36.3],   # Tula area
            [54.3, 13.4],   # Berlin area (Soviet control)
            [54.0, 20.0],   # Gdansk area
            [53.9, 27.6],   # Minsk area
            [53.8, 38.5],   # Kursk area
            [53.2, 34.4],   # Bryansk area
            [52.5, 13.4],   # Berlin (captured)
            [52.2, 21.0],   # Warsaw area
            [52.0, 39.0],   # Voronezh area
            [51.5, 36.2],   # Belgorod area
            [51.1, 17.0],   # Wroclaw area
            [50.8, 14.4],   # Dresden area (Soviet control)
            [50.4, 30.5],   # Kiev area
            [50.1, 14.4],   # Prague (liberated)
            [50.0, 36.6],   # Kharkov area
            [49.6, 36.2],   # Poltava area
            [49.0, 38.0],   # Donetsk area
            [48.7, 44.5],   # Stalingrad area
            [48.5, 35.1],   # Dnipro area
            [48.2, 16.4],   # Vienna area
            [47.8, 35.1],   # Melitopol area
            [47.5, 19.0],   # Budapest area
            [47.1, 39.4],   # Rostov area
            [46.8, 32.0],   # Kherson area
            [46.3, 30.7],   # Odessa area
            [46.1, 14.8],   # Ljubljana area
            [46.0, 30.0],   # Southern Ukraine
            [45.8, 15.9],   # Zagreb area
            [45.3, 28.6],   # Moldavia
            [44.8, 20.4],   # Belgrade area
            [44.4, 26.1],   # Romania
            [43.2, 27.9],   # Bulgaria area
            [42.7, 23.3],   # Sofia area
            [41.9, 12.5]    # Rome area (Allied control)
        ]), 'Eastern')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO ww2_frontlines (date, front_name, coordinates, theater)
        VALUES (?, ?, ?, ?)
    ''', eastern_front_lines)
    
    # Insert Western Front data
    western_front_lines = [
        ('1944-06-06', 'Western Front - D-Day Landings', json.dumps([
            [49.4, -0.4],   # Normandy beaches
            [49.3, -0.5],   # Omaha Beach
            [49.3, -0.3],   # Gold Beach
            [49.3, -0.2],   # Juno Beach
            [49.3, -0.1],   # Sword Beach
            [49.4, -1.2],   # Cherbourg area
            [49.2, -1.0],   # Carentan area
            [49.1, -0.8],   # Bayeux area
            [49.0, -0.4]    # Caen area
        ]), 'Western'),
        
        ('1944-08-25', 'Western Front - Liberation of Paris', json.dumps([
            [50.8, 4.4],    # Brussels approach
            [50.1, 1.8],    # Calais area
            [49.9, 2.3],    # Amiens area
            [49.4, 0.1],    # Le Havre area
            [49.0, 2.3],    # Compiegne area
            [48.9, 2.3],    # Paris (liberated)
            [48.7, 2.4],    # Paris suburbs
            [48.4, 2.7],    # Fontainebleau area
            [48.1, -1.7],   # Rennes area
            [47.9, -1.9],   # Nantes area
            [47.2, -1.6],   # La Rochelle area
            [46.2, 6.1],    # Geneva area
            [45.8, 4.8],    # Lyon area
            [45.2, 5.7],    # Grenoble area
            [43.6, 7.2],    # Nice area
            [43.3, 5.4]     # Marseille area
        ]), 'Western'),
        
        ('1945-03-07', 'Western Front - Rhine Crossing', json.dumps([
            [53.2, 7.0],    # Bremen area
            [52.4, 9.7],    # Hannover area
            [52.0, 8.5],    # Osnabrück area
            [51.5, 7.5],    # Dortmund area
            [51.2, 6.8],    # Düsseldorf area
            [50.9, 6.9],    # Cologne area
            [50.7, 7.1],    # Bonn area
            [50.1, 8.7],    # Frankfurt area
            [49.5, 8.5],    # Mannheim area
            [49.0, 8.4],    # Karlsruhe area
            [48.8, 9.2],    # Stuttgart area
            [48.1, 11.6],   # Munich area
            [47.8, 13.0],   # Salzburg area
            [47.3, 11.4]    # Innsbruck area
        ]), 'Western')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO ww2_frontlines (date, front_name, coordinates, theater)
        VALUES (?, ?, ?, ?)
    ''', western_front_lines)
    
    # Insert more detailed WW2 events
    detailed_events = [
        # 1939 Events
        ('1939-09-01', 'Invasion of Poland Begins', 'German forces cross the Polish border at multiple points, beginning World War II in Europe', 52.2297, 21.0122, 'invasion'),
        ('1939-09-17', 'Soviet Invasion of Poland', 'Soviet forces invade Poland from the east, sealing Poland\'s fate', 52.2297, 21.0122, 'invasion'),
        ('1939-09-27', 'Warsaw Surrenders', 'Polish capital falls to German forces after heroic resistance', 52.2297, 21.0122, 'surrender'),
        
        # 1940 Events
        ('1940-04-09', 'Operation Weserübung', 'Germany invades Denmark and Norway', 59.9139, 10.7522, 'invasion'),
        ('1940-05-10', 'Battle of France Begins', 'German offensive in the west begins', 49.7439, 6.1723, 'battle'),
        ('1940-05-26', 'Dunkirk Evacuation Begins', 'Operation Dynamo - evacuation of Allied forces', 51.0347, 2.3771, 'evacuation'),
        ('1940-06-14', 'Germans Enter Paris', 'German forces occupy the French capital', 48.8566, 2.3522, 'occupation'),
        ('1940-06-22', 'France Signs Armistice', 'France surrenders to Germany at Compiègne', 49.4175, 2.8256, 'surrender'),
        ('1940-07-10', 'Battle of Britain Begins', 'German air offensive against Britain starts', 51.5074, -0.1278, 'battle'),
        ('1940-09-07', 'London Blitz Begins', 'German bombing campaign against London starts', 51.5074, -0.1278, 'bombing'),
        
        # 1941 Events
        ('1941-04-06', 'Invasion of Yugoslavia', 'Axis forces invade Yugoslavia and Greece', 44.7866, 20.4489, 'invasion'),
        ('1941-05-20', 'Battle of Crete', 'German airborne invasion of Crete', 35.2401, 24.8093, 'battle'),
        ('1941-06-22', 'Operation Barbarossa', 'Germany launches massive invasion of Soviet Union', 55.7558, 37.6176, 'invasion'),
        ('1941-07-16', 'Smolensk Encirclement', 'Major German victory in central Russia', 54.7818, 32.0401, 'battle'),
        ('1941-09-08', 'Siege of Leningrad Begins', 'German forces begin 872-day siege of Leningrad', 59.9311, 30.3609, 'siege'),
        ('1941-10-02', 'Operation Typhoon', 'German offensive toward Moscow begins', 55.7558, 37.6176, 'offensive'),
        ('1941-12-06', 'Soviet Winter Counter-offensive', 'Red Army launches counter-attack near Moscow', 55.7558, 37.6176, 'counter-offensive'),
        ('1941-12-07', 'Pearl Harbor Attack', 'Japanese surprise attack brings US into war', 21.3099, -157.8581, 'attack'),
        
        # 1942 Events
        ('1942-01-20', 'Wannsee Conference', 'Nazi officials coordinate the Final Solution', 52.4333, 13.1667, 'conference'),
        ('1942-04-18', 'Doolittle Raid', 'First US air raid on Japanese mainland', 35.6762, 139.6503, 'raid'),
        ('1942-05-04', 'Battle of the Coral Sea', 'First major naval battle fought entirely by aircraft', -15.0, 155.0, 'naval_battle'),
        ('1942-06-04', 'Battle of Midway', 'Decisive US naval victory in the Pacific', 28.2072, -177.3735, 'naval_battle'),
        ('1942-06-28', 'Case Blue Begins', 'German summer offensive toward Stalingrad and Caucasus', 48.7080, 44.5133, 'offensive'),
        ('1942-08-23', 'Battle of Stalingrad Begins', 'German 6th Army reaches Stalingrad', 48.7080, 44.5133, 'battle'),
        ('1942-10-23', 'Second Battle of El Alamein', 'British offensive in North Africa begins', 30.8333, 28.9667, 'battle'),
        ('1942-11-08', 'Operation Torch', 'Allied landings in North Africa', 36.7372, -4.4178, 'landing'),
        ('1942-11-19', 'Operation Uranus', 'Soviet counter-offensive at Stalingrad begins', 48.7080, 44.5133, 'counter-offensive'),
        
        # 1943 Events
        ('1943-01-14', 'Casablanca Conference', 'Roosevelt and Churchill meet in Morocco', 33.5731, -7.5898, 'conference'),
        ('1943-02-02', 'Stalingrad Victory', 'German 6th Army surrenders at Stalingrad', 48.7080, 44.5133, 'victory'),
        ('1943-04-19', 'Warsaw Ghetto Uprising', 'Jewish resistance in Warsaw ghetto begins', 52.2297, 21.0122, 'uprising'),
        ('1943-05-13', 'Tunisia Campaign Ends', 'Axis forces in North Africa surrender', 36.8065, 10.1815, 'surrender'),
        ('1943-07-05', 'Battle of Kursk', 'Largest tank battle in history begins', 51.7373, 36.1873, 'battle'),
        ('1943-07-10', 'Allied Invasion of Sicily', 'Operation Husky begins', 37.5079, 15.0830, 'invasion'),
        ('1943-09-03', 'Italy Surrenders', 'Italian government signs armistice with Allies', 41.9028, 12.4964, 'surrender'),
        ('1943-09-09', 'Salerno Landings', 'Allied invasion of Italian mainland', 40.6824, 14.7681, 'landing'),
        ('1943-11-06', 'Kiev Liberated', 'Red Army recaptures Ukrainian capital', 50.4501, 30.5234, 'liberation'),
        
        # 1944 Events
        ('1944-01-27', 'Siege of Leningrad Ends', 'Red Army breaks 872-day siege', 59.9311, 30.3609, 'liberation'),
        ('1944-03-19', 'Germany Occupies Hungary', 'Operation Margarethe begins', 47.4979, 19.0402, 'occupation'),
        ('1944-06-04', 'Rome Liberated', 'Allied forces enter the Eternal City', 41.9028, 12.4964, 'liberation'),
        ('1944-06-06', 'D-Day Normandy Landings', 'Operation Overlord - largest seaborne invasion in history', 49.3967, -0.4431, 'invasion'),
        ('1944-06-23', 'Operation Bagration', 'Massive Soviet offensive destroys Army Group Center', 53.9006, 27.5590, 'offensive'),
        ('1944-07-20', 'July 20 Plot', 'Failed assassination attempt on Hitler', 54.0924, 12.1342, 'assassination_attempt'),
        ('1944-08-01', 'Warsaw Uprising', 'Polish Home Army rises against German occupation', 52.2297, 21.0122, 'uprising'),
        ('1944-08-15', 'Operation Dragoon', 'Allied invasion of southern France', 43.2695, 6.6407, 'invasion'),
        ('1944-08-23', 'Romania Switches Sides', 'Romania joins the Allies', 44.4268, 26.1025, 'defection'),
        ('1944-08-25', 'Paris Liberated', 'Allied forces enter the French capital', 48.8566, 2.3522, 'liberation'),
        ('1944-09-17', 'Operation Market Garden', 'Failed Allied airborne operation in Netherlands', 51.9851, 5.8987, 'operation'),
                ('1944-10-20', 'Belgrade Liberated', 'Soviet and Yugoslav forces liberate Serbian capital', 44.7866, 20.4489, 'liberation'),
        ('1944-12-16', 'Battle of the Bulge', 'German counter-offensive in Ardennes begins', 50.4274, 5.7939, 'battle'),
        
        # 1945 Events
        ('1945-01-12', 'Vistula-Oder Offensive', 'Massive Soviet offensive toward Berlin begins', 52.2297, 21.0122, 'offensive'),
        ('1945-01-17', 'Warsaw Liberated', 'Red Army liberates devastated Polish capital', 52.2297, 21.0122, 'liberation'),
        ('1945-01-27', 'Auschwitz Liberated', 'Soviet forces liberate the death camp', 50.0347, 19.2041, 'liberation'),
        ('1945-02-04', 'Yalta Conference', 'Roosevelt, Churchill, and Stalin meet in Crimea', 44.4952, 34.1742, 'conference'),
        ('1945-02-13', 'Dresden Bombing', 'Allied bombing devastates German city', 51.0504, 13.7373, 'bombing'),
        ('1945-03-07', 'Remagen Bridge Captured', 'US forces capture intact Rhine bridge', 50.5791, 7.2461, 'capture'),
        ('1945-04-12', 'Roosevelt Dies', 'US President Franklin D. Roosevelt dies', 32.8907, -84.8803, 'death'),
        ('1945-04-16', 'Battle of Berlin Begins', 'Final Soviet assault on Nazi capital starts', 52.5200, 13.4050, 'battle'),
        ('1945-04-25', 'Elbe Meeting', 'US and Soviet forces meet at Torgau', 51.5606, 12.9922, 'meeting'),
        ('1945-04-28', 'Mussolini Executed', 'Italian dictator killed by partisans', 45.8566, 9.2308, 'execution'),
        ('1945-04-30', 'Hitler Commits Suicide', 'Nazi leader kills himself in Berlin bunker', 52.5200, 13.4050, 'suicide'),
        ('1945-05-02', 'Berlin Falls', 'Soviet forces capture the German capital', 52.5200, 13.4050, 'capture'),
        ('1945-05-08', 'VE Day', 'Germany surrenders unconditionally - Victory in Europe', 52.5200, 13.4050, 'victory'),
        ('1945-08-06', 'Hiroshima Atomic Bomb', 'First atomic bomb dropped on Japan', 34.3853, 132.4553, 'atomic_bomb'),
        ('1945-08-09', 'Nagasaki Atomic Bomb', 'Second atomic bomb dropped on Japan', 32.7503, 129.8779, 'atomic_bomb'),
        ('1945-08-09', 'Soviet Invasion of Manchuria', 'USSR enters war against Japan', 43.8171, 125.2992, 'invasion'),
        ('1945-08-15', 'Japan Surrenders', 'Emperor announces surrender - VJ Day', 35.6762, 139.6503, 'surrender'),
        ('1945-09-02', 'Formal Japanese Surrender', 'Surrender ceremony aboard USS Missouri', 35.6762, 139.6503, 'ceremony')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO ww2_events (date, title, description, latitude, longitude, event_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', detailed_events)
    
    # Insert sample veterans with more detailed information
    detailed_veterans = [
        ('Жуков Георгий Константинович', '1896-12-01', '1974-06-18', None,
         'Маршал Советского Союза, четырежды Герой Советского Союза. Командовал обороной Ленинграда, битвой за Москву, Сталинградской битвой, штурмом Берлина.',
         20, '1-й Белорусский фронт', 'Герой Советского Союза (4 раза), Орден "Победа" (2 раза), Орден Ленина (6 раз)',
         'Оборона Ленинграда, Битва за Москву, Сталинградская битва, Курская битва, Штурм Берлина'),
        
        ('Рокоссовский Константин Константинович', '1896-12-21', '1968-08-03', None,
         'Маршал Советского Союза, дважды Герой Советского Союза. Командовал Центральным фронтом в Курской битве, 1-м Белорусским фронтом.',
         20, '1-й Белорусский фронт', 'Герой Советского Союза (2 раза), Орден "Победа", Орден Ленина (7 раз)',
         'Битва за Москву, Сталинградская битва, Курская битва, Операция "Багратион"'),
        
        ('Василевский Александр Михайлович', '1895-09-30', '1977-12-05', None,
         'Маршал Советского Союза, дважды Герой Советского Союза. Начальник Генерального штаба, один из главных стратегов Великой Отечественной войны.',
         20, 'Генеральный штаб РККА', 'Герой Советского Союза (2 раза), Орден "Победа", Орден Ленина (8 раз)',
         'Сталинградская битва, Курская битва, Операция "Багратион", Маньчжурская операция'),
        
        ('Конев Иван Степанович', '1897-12-28', '1973-05-21', None,
         'Маршал Советского Союза, дважды Герой Советского Союза. Командовал 1-м Украинским фронтом, освобождал Украину, Польшу, Чехословакию.',
         20, '1-й Украинский фронт', 'Герой Советского Союза (2 раза), Орден "Победа", Орден Ленина (7 раз)',
         'Битва за Москву, Курская битва, Корсунь-Шевченковская операция, Берлинская операция'),
        
        ('Малиновский Родион Яковлевич', '1898-11-23', '1967-03-31', None,
         'Маршал Советского Союза, дважды Герой Советского Союза. Командовал 2-м и 3-м Украинскими фронтами.',
         20, '2-й Украинский фронт', 'Герой Советского Союза (2 раза), Орден "Победа", Орден Ленина (5 раз)',
         'Сталинградская битва, Донбасская операция, Ясско-Кишиневская операция, Будапештская операция'),
        
        ('Толбухин Федор Иванович', '1894-06-16', '1949-10-17', None,
         'Маршал Советского Союза, Герой Советского Союза. Командовал 3-м Украинским фронтом, освобождал Крым, Болгарию, Югославию.',
         20, '3-й Украинский фронт', 'Герой Советского Союза, Орден "Победа", Орден Ленина (4 раза)',
         'Сталинградская битва, Освобождение Крыма, Ясско-Кишиневская операция, Венская операция'),
        
        ('Говоров Леонид Александрович', '1897-02-22', '1955-03-19', None,
         'Маршал Советского Союза, Герой Советского Союза. Командовал Ленинградским фронтом, руководил прорывом блокады Ленинграда.',
         20, 'Ленинградский фронт', 'Герой Советского Союза, Орден "Победа", Орден Ленина (5 раз)',
         'Оборона Москвы, Оборона Ленинграда, Прорыв блокады Ленинграда'),
        
        ('Мерецков Кирилл Афанасьевич', '1897-06-07', '1968-12-30', None,
         'Маршал Советского Союза, Герой Советского Союза. Командовал Волховским и Карельским фронтами.',
         20, 'Карельский фронт', 'Герой Советского Союза, Орден "Победа", Орден Ленина (7 раз)',
         'Советско-финская война, Любанская операция, Свирско-Петрозаводская операция'),
        
        ('Баграмян Иван Христофорович', '1897-12-02', '1982-09-21', None,
         'Маршал Советского Союза, дважды Герой Советского Союза. Командовал 1-м Прибалтийским фронтом.',
         20, '1-й Прибалтийский фронт', 'Герой Советского Союза (2 раза), Орден "Победа", Орден Ленина (8 раз)',
         'Курская битва, Операция "Багратион", Освобождение Прибалтики'),
        
        ('Черняховский Иван Данилович', '1907-06-29', '1945-02-18', None,
         'Генерал армии, дважды Герой Советского Союза. Самый молодой командующий фронтом. Погиб в Восточно-Прусской операции.',
         18, '3-й Белорусский фронт', 'Герой Советского Союза (2 раза), Орден Ленина (3 раза), Орден Красного Знамени (4 раза)',
         'Курская битва, Операция "Багратион", Восточно-Прусская операция'),
        
        # Добавим рядовых солдат и сержантов
        ('Матросов Александр Матвеевич', '1924-02-05', '1943-02-23', None,
         'Гвардии рядовой, Герой Советского Союза. Закрыл своим телом амбразуру вражеского дзота, обеспечив успех атаки.',
         1, '254-й гвардейский стрелковый полк', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Северо-Западный фронт, бои у деревни Чернушки'),
        
        ('Космодемьянская Зоя Анатольевна', '1923-09-13', '1941-11-29', None,
         'Партизанка, разведчица, Герой Советского Союза. Казнена немцами в деревне Петрищево.',
         1, 'Партизанский отряд', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Партизанская деятельность в Подмосковье'),
        
        ('Гастелло Николай Францевич', '1907-05-06', '1941-06-26', None,
         'Капитан, Герой Советского Союза. Направил горящий самолет на колонну вражеской техники.',
         12, '207-й дальнебомбардировочный авиационный полк', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Оборонительные бои 1941 года'),
        
        ('Талалихин Виктор Васильевич', '1918-09-18', '1941-10-27', None,
         'Младший лейтенант, Герой Советского Союза. Первый летчик, совершивший ночной таран.',
         9, '177-й истребительный авиационный полк', 'Герой Советского Союза, Орден Ленина, Орден Красного Знамени',
         'Оборона Москвы, воздушные бои'),
        
        ('Покрышкин Александр Иванович', '1913-03-06', '1985-11-13', None,
         'Маршал авиации, трижды Герой Советского Союза. Сбил 59 самолетов противника.',
         19, '16-й гвардейский истребительный авиационный полк', 'Герой Советского Союза (3 раза), Орден Ленина (6 раз)',
         'Воздушные бои на всех фронтах'),
        
        ('Кожедуб Иван Никитович', '1920-06-08', '1991-08-08', None,
         'Маршал авиации, трижды Герой Советского Союза. Самый результативный летчик-истребитель союзников - 62 победы.',
         19, '176-й гвардейский истребительный авиационный полк', 'Герой Советского Союза (3 раза), Орден Ленина (2 раза)',
         'Воздушные бои, Курская битва, освобождение Украины'),
        
        ('Маресьев Алексей Петрович', '1916-05-20', '2001-05-18', None,
         'Старший лейтенант, Герой Советского Союза. После ампутации ног продолжал летать и сбивать вражеские самолеты.',
         11, '63-й гвардейский истребительный авиационный полк', 'Герой Советского Союза, Орден Ленина, Орден Красного Знамени (2 раза)',
         'Воздушные бои, Курская битва'),
        
                ('Карбышев Дмитрий Михайлович', '1880-10-26', '1945-02-18', None,
         'Генерал-лейтенант инженерных войск, Герой Советского Союза. Замучен в концлагере Маутхаузен.',
         17, 'Инженерные войска', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Оборонительные бои 1941 года, узник концлагерей'),
        
        ('Панфилов Иван Васильевич', '1893-11-01', '1941-11-19', None,
         'Генерал-майор, Герой Советского Союза. Командир 316-й стрелковой дивизии, погиб в бою под Москвой.',
         16, '316-я стрелковая дивизия', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Оборона Москвы, Волоколамское направление'),
        
        ('Клочков Василий Георгиевич', '1911-03-08', '1941-11-16', None,
         'Политрук, Герой Советского Союза. Один из 28 панфиловцев, произнес знаменитые слова: "Велика Россия, а отступать некуда - позади Москва!"',
         7, '1075-й стрелковый полк', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Оборона Москвы, бой у разъезда Дубосеково'),
        
        ('Молодогвардейцы - Олег Кошевой', '1926-06-08', '1943-02-09', None,
         'Руководитель подпольной организации "Молодая гвардия", Герой Советского Союза.',
         1, 'Подпольная организация "Молодая гвардия"', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Подпольная деятельность в оккупированном Краснодоне'),
        
        ('Молодогвардейцы - Зоя Космодемьянская', '1923-09-13', '1941-11-29', None,
         'Партизанка-разведчица, первая женщина - Герой Советского Союза в ВОВ.',
         1, 'Партизанский отряд 9903 войсковой части', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Партизанская деятельность в Подмосковье'),
        
        ('Девятаев Михаил Петрович', '1917-07-08', '2002-11-24', None,
         'Старший лейтенант, Герой Советского Союза. Совершил побег из концлагеря на угнанном немецком самолете.',
         11, '104-й истребительный авиационный полк', 'Герой Советского Союза, Орден Ленина',
         'Воздушные бои, побег из концлагеря Пенемюнде'),
        
        ('Руднев Сергей Васильевич', '1921-05-15', '1943-07-19', None,
         'Сержант, Герой Советского Союза. Повторил подвиг Матросова в Курской битве.',
         4, '895-й стрелковый полк', 'Герой Советского Союза (посмертно), Орден Ленина',
         'Курская битва, бои на Орловско-Курской дуге'),
        
        ('Смирнов Алексей Петрович', '1920-03-12', '1944-08-15', None,
         'Старший сержант, участник обороны Сталинграда. Награжден орденом Красной Звезды.',
         5, '62-я армия', 'Орден Красной Звезды, Медаль "За оборону Сталинграда"',
         'Сталинградская битва, уличные бои'),
        
        ('Петров Николай Иванович', '1918-11-07', '1945-01-20', None,
         'Младший лейтенант, командир танкового взвода. Участник освобождения Польши.',
         9, '1-я гвардейская танковая армия', 'Орден Отечественной войны I степени, Орден Красной Звезды',
         'Курская битва, Освобождение Украины, Висло-Одерская операция'),
        
        ('Сидоров Василий Степанович', '1922-04-25', '1943-12-03', None,
         'Рядовой, пулеметчик. Героически погиб при форсировании Днепра.',
         1, '150-я стрелковая дивизия', 'Орден Красного Знамени (посмертно), Медаль "За отвагу"',
         'Битва за Днепр, форсирование реки'),
        
        ('Козлов Иван Федорович', '1919-08-30', '1944-06-23', None,
         'Старшина, командир отделения разведки. Погиб в операции "Багратион".',
         6, '3-я армия', 'Орден Славы III степени, Орден Красной Звезды',
         'Операция "Багратион", разведывательные рейды'),
        
        ('Волков Михаил Александрович', '1920-12-15', '1945-04-25', None,
         'Лейтенант, командир стрелкового взвода. Погиб в боях за Берлин.',
         10, '8-я гвардейская армия', 'Орден Отечественной войны II степени, Орден Красной Звезды',
         'Сталинградская битва, Берлинская операция'),
        
        ('Морозов Федор Григорьевич', '1921-01-18', '1943-09-26', None,
         'Сержант, наводчик противотанкового орудия. Подбил 8 немецких танков.',
         4, '13-я гвардейская стрелковая дивизия', 'Орден Красного Знамени, Медаль "За отвагу"',
         'Курская битва, противотанковая оборона'),
        
        ('Белов Григорий Семенович', '1923-06-10', '1944-07-15', None,
         'Младший сержант, связист. Обеспечивал связь в критических ситуациях.',
         3, '11-я гвардейская армия', 'Орден Красной Звезды, Медаль "За боевые заслуги"',
         'Операция "Багратион", обеспечение связи'),
        
        ('Новиков Павел Васильевич', '1920-09-03', '1943-11-12', None,
         'Старший сержант, командир саперного отделения. Обезвредил множество мин.',
         5, '1-я саперная бригада', 'Орден Красной Звезды, Медаль "За отвагу"',
         'Битва за Днепр, инженерное обеспечение'),
        
        ('Орлов Анатолий Петрович', '1922-02-28', '1945-02-14', None,
         'Рядовой, автоматчик. Участник штурма Кенигсберга.',
         1, '11-я гвардейская армия', 'Медаль "За отвагу", Медаль "За боевые заслуги"',
         'Восточно-Прусская операция, штурм Кенигсберга'),
        
        ('Соколов Владимир Николаевич', '1921-07-22', '1944-10-08', None,
         'Младший лейтенант, командир минометного взвода. Погиб в боях в Прибалтике.',
         9, '2-я ударная армия', 'Орден Отечественной войны II степени',
         'Освобождение Прибалтики, бои в Латвии'),
        
        ('Кузнецов Дмитрий Иванович', '1919-05-17', '1943-08-05', None,
         'Сержант, командир пулеметного расчета. Героически сражался на Курской дуге.',
         4, '70-я армия', 'Орден Красного Знамени, Орден Красной Звезды',
         'Курская битва, оборонительные бои'),
        
        ('Лебедев Александр Федорович', '1920-10-11', '1944-01-28', None,
         'Старшина, командир отделения автоматчиков. Участник прорыва блокады Ленинграда.',
         6, '67-я армия', 'Орден Красной Звезды, Медаль "За оборону Ленинграда"',
         'Прорыв блокады Ленинграда, Новгородско-Лужская операция'),
        
        ('Медведев Сергей Николаевич', '1918-12-04', '1945-05-02', None,
         'Капитан, командир стрелковой роты. Дошел до Берлина.',
         12, '1-я гвардейская танковая армия', 'Орден Отечественной войны I степени, Орден Красного Знамени',
         'От Сталинграда до Берлина, штурм рейхстага')
    ]
    
    for veteran_data in detailed_veterans:
        cursor.execute('''
            INSERT OR IGNORE INTO veterans 
            (full_name, birth_date, death_date, photo_path, biography, position_id, unit, awards, battles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', veteran_data)
    
    db.commit()

# Add more API endpoints for statistics and analytics
@app.route('/api/statistics/overview', methods=['GET'])
def get_statistics_overview():
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get comprehensive statistics
        stats = {}
        
        # User statistics
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE is_active = 1')
        stats['active_users'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE created_at >= date("now", "-30 days")')
        stats['new_users_month'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = "admin"')
        stats['admin_users'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE role = "moderator"')
        stats['moderator_users'] = cursor.fetchone()['total']
        
        # Recording statistics
        cursor.execute('SELECT COUNT(*) as total FROM recordings')
        stats['total_recordings'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM recordings WHERE created_at >= date("now", "-30 days")')
        stats['new_recordings_month'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT SUM(views) as total FROM recordings')
        stats['total_views'] = cursor.fetchone()['total'] or 0
        
        cursor.execute('SELECT AVG(views) as avg FROM recordings')
        stats['avg_views_per_recording'] = round(cursor.fetchone()['avg'] or 0, 2)
        
        # Category statistics
        cursor.execute('SELECT COUNT(*) as total FROM categories')
        stats['total_categories'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM tags')
        stats['total_tags'] = cursor.fetchone()['total']
        
        # Veterans statistics
        cursor.execute('SELECT COUNT(*) as total FROM veterans')
        stats['total_veterans'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM veterans WHERE death_date IS NOT NULL')
        stats['fallen_veterans'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM military_positions')
        stats['military_positions'] = cursor.fetchone()['total']
        
        # WW2 data statistics
        cursor.execute('SELECT COUNT(*) as total FROM ww2_events')
        stats['ww2_events'] = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM ww2_frontlines')
        stats['ww2_frontlines'] = cursor.fetchone()['total']
        
        # Most popular categories
        cursor.execute('''
            SELECT c.name, COUNT(r.id) as count
            FROM categories c
            LEFT JOIN recordings r ON c.id = r.category_id
            GROUP BY c.id, c.name
            ORDER BY count DESC
            LIMIT 5
        ''')
        stats['popular_categories'] = [dict(row) for row in cursor.fetchall()]
        
        # Most active users
        cursor.execute('''
            SELECT u.username, COUNT(r.id) as recording_count
            FROM users u
            LEFT JOIN recordings r ON u.id = r.author_id
            WHERE u.is_active = 1
            GROUP BY u.id, u.username
            ORDER BY recording_count DESC
            LIMIT 5
        ''')
        stats['active_users_list'] = [dict(row) for row in cursor.fetchall()]
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"Get statistics overview error: {e}")
        return jsonify({'message': 'Failed to fetch statistics'}), 500

@app.route('/api/statistics/veterans-by-rank', methods=['GET'])
def get_veterans_by_rank():
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT mp.name, mp.rank_level, COUNT(v.id) as count
            FROM military_positions mp
            LEFT JOIN veterans v ON mp.id = v.position_id
            GROUP BY mp.id, mp.name, mp.rank_level
            ORDER BY mp.rank_level DESC
        ''')
        result = [dict(row) for row in cursor.fetchall()]
        return jsonify(result)
        
    except Exception as e:
        print(f"Get veterans by rank error: {e}")
        return jsonify({'message': 'Failed to fetch veterans by rank'}), 500

@app.route('/api/statistics/events-by-year', methods=['GET'])
def get_events_by_year():
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT 
                substr(date, 1, 4) as year,
                COUNT(*) as event_count,
                COUNT(CASE WHEN event_type = 'battle' THEN 1 END) as battles,
                COUNT(CASE WHEN event_type = 'victory' THEN 1 END) as victories,
                COUNT(CASE WHEN event_type = 'liberation' THEN 1 END) as liberations
            FROM ww2_events
            GROUP BY substr(date, 1, 4)
            ORDER BY year
        ''')
        
        result = [dict(row) for row in cursor.fetchall()]
        return jsonify(result)
        
    except Exception as e:
        print(f"Get events by year error: {e}")
        return jsonify({'message': 'Failed to fetch events by year'}), 500

@app.route('/api/statistics/recordings-activity', methods=['GET'])
def get_recordings_activity():
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get recordings created per month for the last 12 months
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', created_at) as month,
                COUNT(*) as count
            FROM recordings
            WHERE created_at >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', created_at)
            ORDER BY month
        ''')
        
        monthly_data = [dict(row) for row in cursor.fetchall()]
        
        # Get recordings by category
        cursor.execute('''
            SELECT c.name, COUNT(r.id) as count
            FROM categories c
            LEFT JOIN recordings r ON c.id = r.category_id
            GROUP BY c.id, c.name
            ORDER BY count DESC
        ''')
        
        category_data = [dict(row) for row in cursor.fetchall()]
        
        # Get most viewed recordings
        cursor.execute('''
            SELECT r.title, r.views, u.username as author
            FROM recordings r
            LEFT JOIN users u ON r.author_id = u.id
            ORDER BY r.views DESC
            LIMIT 10
        ''')
        
        top_recordings = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'monthly_activity': monthly_data,
            'category_distribution': category_data,
            'top_recordings': top_recordings
        })
        
    except Exception as e:
        print(f"Get recordings activity error: {e}")
        return jsonify({'message': 'Failed to fetch recordings activity'}), 500

@app.route('/api/search', methods=['GET'])
def global_search():
    try:
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all')  # all, recordings, veterans, events
        limit = int(request.args.get('limit', 20))
        
        if not query:
            return jsonify({'message': 'Search query is required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        results = {}
        
        # Search recordings
        if search_type in ['all', 'recordings']:
            cursor.execute('''
                SELECT r.id, r.title, r.content, r.created_at, r.views,
                       c.name as category_name, u.username as author_username
                FROM recordings r
                LEFT JOIN categories c ON r.category_id = c.id
                LEFT JOIN users u ON r.author_id = u.id
                WHERE r.title LIKE ? OR r.content LIKE ?
                ORDER BY r.views DESC, r.created_at DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', limit))
            
            recordings = []
            for row in cursor.fetchall():
                recordings.append({
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'][:200] + '...' if len(row['content']) > 200 else row['content'],
                    'category': row['category_name'],
                    'author': row['author_username'],
                    'created_at': row['created_at'],
                    'views': row['views'],
                    'type': 'recording'
                })
            results['recordings'] = recordings
        
        # Search veterans
        if search_type in ['all', 'veterans']:
            cursor.execute('''
                SELECT v.id, v.full_name, v.birth_date, v.death_date, v.biography,
                       v.unit, v.awards, v.battles, mp.name as position_name
                FROM veterans v
                LEFT JOIN military_positions mp ON v.position_id = mp.id
                WHERE v.full_name LIKE ? OR v.biography LIKE ? OR v.unit LIKE ? OR v.battles LIKE ?
                ORDER BY v.full_name
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', limit))
            
            veterans = []
            for row in cursor.fetchall():
                veterans.append({
                    'id': row['id'],
                    'full_name': row['full_name'],
                    'birth_date': row['birth_date'],
                    'death_date': row['death_date'],
                    'biography': row['biography'][:200] + '...' if row['biography'] and len(row['biography']) > 200 else row['biography'],
                    'position': row['position_name'],
                    'unit': row['unit'],
                    'awards': row['awards'],
                    'battles': row['battles'],
                    'type': 'veteran'
                })
            results['veterans'] = veterans
        
        # Search WW2 events
        if search_type in ['all', 'events']:
            cursor.execute('''
                SELECT id, date, title, description, event_type, latitude, longitude
                FROM ww2_events
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY date
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', limit))
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    'id': row['id'],
                    'date': row['date'],
                    'title': row['title'],
                    'description': row['description'][:200] + '...' if len(row['description']) > 200 else row['description'],
                    'event_type': row['event_type'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'type': 'event'
                })
            results['events'] = events
        
        # Search users (if admin)
        if search_type in ['all', 'users']:
            # Only include user search for authenticated admin users
            try:
                from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
                verify_jwt_in_request(optional=True)
                current_user_id = get_jwt_identity()
                
                if current_user_id:
                    cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
                    user = cursor.fetchone()
                    
                    if user and user['role'] in ['admin', 'moderator']:
                        cursor.execute('''
                            SELECT id, username, email, role, created_at, is_active
                            FROM users
                            WHERE username LIKE ? OR email LIKE ?
                            ORDER BY username
                            LIMIT ?
                        ''', (f'%{query}%', f'%{query}%', limit))
                        
                        users = []
                        for row in cursor.fetchall():
                            users.append({
                                'id': row['id'],
                                'username': row['username'],
                                'email': row['email'],
                                'role': row['role'],
                                'created_at': row['created_at'],
                                'is_active': row['is_active'],
                                'type': 'user'
                            })
                        results['users'] = users
            except:
                pass  # No user search for non-authenticated users
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Global search error: {e}")
        return jsonify({'message': 'Search failed'}), 500

# Add export functionality
@app.route('/api/export/veterans', methods=['GET'])
@jwt_required()
def export_veterans():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Get all veterans data
        cursor.execute('''
            SELECT v.*, mp.name as position_name, mp.rank_level
            FROM veterans v
            LEFT JOIN military_positions mp ON v.position_id = mp.id
            ORDER BY v.full_name
        ''')
        
        veterans = cursor.fetchall()
        
        # Convert to list of dictionaries
        veterans_data = []
        for veteran in veterans:
            veterans_data.append({
                'ID': veteran['id'],
                'Полное имя': veteran['full_name'],
                'Дата рождения': veteran['birth_date'],
                'Дата смерти': veteran['death_date'],
                'Воинское звание': veteran['position_name'],
                'Уровень звания': veteran['rank_level'],
                'Воинская часть': veteran['unit'],
                'Биография': veteran['biography'],
                'Награды': veteran['awards'],
                'Участие в боях': veteran['battles'],
                'Дата создания записи': veteran['created_at']
            })
        
        return jsonify({
            'data': veterans_data,
            'total': len(veterans_data),
            'exported_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Export veterans error: {e}")
        return jsonify({'message': 'Failed to export veterans data'}), 500

@app.route('/api/export/events', methods=['GET'])
@jwt_required()
def export_events():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Get all events data
        cursor.execute('''
            SELECT * FROM ww2_events
            ORDER BY date, title
        ''')
        
        events = cursor.fetchall()
        
        # Convert to list of dictionaries
        events_data = []
        for event in events:
            events_data.append({
                'ID': event['id'],
                'Дата': event['date'],
                'Название': event['title'],
                'Описание': event['description'],
                'Тип события': event['event_type'],
                'Широта': event['latitude'],
                'Долгота': event['longitude'],
                'Дата создания записи': event['created_at']
            })
        
        return jsonify({
            'data': events_data,
            'total': len(events_data),
            'exported_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Export events error: {e}")
        return jsonify({'message': 'Failed to export events data'}), 500

# Add backup and restore functionality
@app.route('/api/admin/backup', methods=['POST'])
@jwt_required()
def create_backup():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check admin permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        # Create backup filename
        backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(app.config['UPLOAD_FOLDER'], backup_filename)
        
        # Copy database file
        import shutil
        shutil.copy2(app.config['DATABASE'], backup_path)
        
        # Log the backup creation
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (int(current_user_id), 'backup', 'База данных скопирована', 
              f'Создана резервная копия: {backup_filename}'))
        
        db.commit()
        
        return jsonify({
            'message': 'Backup created successfully',
            'filename': backup_filename,
            'path': f'/uploads/{backup_filename}',
            'created_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Create backup error: {e}")
        return jsonify({'message': 'Failed to create backup'}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT 1')
        cursor.fetchone()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
        
    except Exception as e:
        print(f"Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Add system information endpoint
@app.route('/api/admin/system-info', methods=['GET'])
@jwt_required()
def get_system_info():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check admin permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        import platform
        import psutil
        
        # Get system information
        system_info = {
            'platform': {
                'system': platform.system(),
                                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version()
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            },
            'cpu': {
                'count': psutil.cpu_count(),
                'percent': psutil.cpu_percent(interval=1)
            }
        }
        
        # Get database size
        db_size = os.path.getsize(app.config['DATABASE'])
        system_info['database'] = {
            'size_bytes': db_size,
            'size_mb': round(db_size / (1024 * 1024), 2)
        }
        
        # Get upload folder size
        upload_size = 0
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for dirpath, dirnames, filenames in os.walk(app.config['UPLOAD_FOLDER']):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    upload_size += os.path.getsize(filepath)
        
        system_info['uploads'] = {
            'size_bytes': upload_size,
            'size_mb': round(upload_size / (1024 * 1024), 2)
        }
        
        return jsonify(system_info)
        
    except Exception as e:
        print(f"Get system info error: {e}")
        return jsonify({'message': 'Failed to get system information'}), 500

# Add database maintenance endpoints
@app.route('/api/admin/maintenance/vacuum', methods=['POST'])
@jwt_required()
def vacuum_database():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check admin permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get database size before vacuum
        size_before = os.path.getsize(app.config['DATABASE'])
        
        # Perform VACUUM
        cursor.execute('VACUUM')
        db.commit()
        
        # Get database size after vacuum
        size_after = os.path.getsize(app.config['DATABASE'])
        space_saved = size_before - size_after
        
        # Log the maintenance activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (int(current_user_id), 'maintenance', 'База данных оптимизирована', 
              f'VACUUM выполнен. Освобождено: {round(space_saved / 1024, 2)} KB'))
        
        db.commit()
        
        return jsonify({
            'message': 'Database vacuum completed successfully',
            'size_before_mb': round(size_before / (1024 * 1024), 2),
            'size_after_mb': round(size_after / (1024 * 1024), 2),
            'space_saved_mb': round(space_saved / (1024 * 1024), 2)
        })
        
    except Exception as e:
        print(f"Vacuum database error: {e}")
        return jsonify({'message': 'Failed to vacuum database'}), 500

@app.route('/api/admin/maintenance/analyze', methods=['POST'])
@jwt_required()
def analyze_database():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check admin permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        # Perform ANALYZE
        cursor.execute('ANALYZE')
        db.commit()
        
        # Log the maintenance activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (int(current_user_id), 'maintenance', 'Статистика БД обновлена', 
              'ANALYZE выполнен для оптимизации запросов'))
        
        db.commit()
        
        return jsonify({'message': 'Database analysis completed successfully'})
        
    except Exception as e:
        print(f"Analyze database error: {e}")
        return jsonify({'message': 'Failed to analyze database'}), 500

# Add file cleanup endpoint
@app.route('/api/admin/cleanup/orphaned-files', methods=['POST'])
@jwt_required()
def cleanup_orphaned_files():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check admin permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (int(current_user_id),))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get all file paths from database
        db_files = set()
        
        # Get recording files
        cursor.execute('SELECT image_path, video_path FROM recordings WHERE image_path IS NOT NULL OR video_path IS NOT NULL')
        for row in cursor.fetchall():
            if row['image_path']:
                db_files.add(os.path.basename(row['image_path']))
            if row['video_path']:
                db_files.add(os.path.basename(row['video_path']))
        
        # Get user avatars
        cursor.execute('SELECT avatar FROM users WHERE avatar IS NOT NULL')
        for row in cursor.fetchall():
            if row['avatar']:
                db_files.add(os.path.basename(row['avatar']))
        
        # Get veteran photos
        cursor.execute('SELECT photo_path FROM veterans WHERE photo_path IS NOT NULL')
        for row in cursor.fetchall():
            if row['photo_path']:
                db_files.add(os.path.basename(row['photo_path']))
        
        # Get all files in upload directory
        upload_files = set()
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    upload_files.add(filename)
        
        # Find orphaned files
        orphaned_files = upload_files - db_files
        
        # Remove orphaned files
        removed_count = 0
        removed_size = 0
        
        for filename in orphaned_files:
            # Skip backup files and system files
            if filename.startswith('backup_') or filename.startswith('.'):
                continue
                
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                removed_count += 1
                removed_size += file_size
            except Exception as e:
                print(f"Failed to remove {filename}: {e}")
        
        # Log the cleanup activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (int(current_user_id), 'maintenance', 'Очистка файлов выполнена', 
              f'Удалено {removed_count} файлов, освобождено {round(removed_size / 1024, 2)} KB'))
        
        db.commit()
        
        return jsonify({
            'message': 'Orphaned files cleanup completed',
            'removed_files': removed_count,
            'space_freed_mb': round(removed_size / (1024 * 1024), 2),
            'orphaned_files': list(orphaned_files)
        })
        
    except Exception as e:
        print(f"Cleanup orphaned files error: {e}")
        return jsonify({'message': 'Failed to cleanup orphaned files'}), 500

# Add API rate limiting information
@app.route('/api/info', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Faculty Management System API',
        'version': '1.0.0',
        'description': 'API for managing faculty recordings, veterans data, and WW2 historical information',
        'endpoints': {
            'authentication': [
                'POST /api/register',
                'POST /api/login'
            ],
            'recordings': [
                'GET /api/recordings',
                'POST /api/recordings/create',
                'GET /api/recordings/{id}',
                'PUT /api/recordings/{id}/update',
                'DELETE /api/recordings/{id}/delete'
            ],
            'veterans': [
                'GET /api/veterans',
                'POST /api/veterans/create',
                'GET /api/veterans/{id}',
                'PUT /api/veterans/{id}/update',
                'DELETE /api/veterans/{id}/delete'
            ],
            'ww2_data': [
                'GET /api/ww2/events',
                'GET /api/ww2/frontlines',
                'GET /api/ww2/timeline'
            ],
            'user_management': [
                'GET /api/users/{id}',
                'GET /api/user/settings',
                'PUT /api/user/settings',
                'PUT /api/user/profile',
                'POST /api/user/change-password',
                'POST /api/user/avatar'
            ],
            'statistics': [
                'GET /api/statistics/overview',
                'GET /api/statistics/veterans-by-rank',
                'GET /api/statistics/events-by-year',
                'GET /api/statistics/recordings-activity'
            ],
            'search': [
                'GET /api/search'
            ],
            'admin': [
                'GET /api/admin/system-info',
                'POST /api/admin/backup',
                'POST /api/admin/maintenance/vacuum',
                'POST /api/admin/maintenance/analyze',
                'POST /api/admin/cleanup/orphaned-files'
            ]
        },
        'features': [
            'JWT Authentication',
            'Role-based Access Control',
            'File Upload Support',
            'Full-text Search',
            'Data Export',
            'System Monitoring',
            'Database Maintenance',
            'Interactive WW2 Map',
            'Veterans Memorial Pages'
        ]
    })

# Add CORS preflight handling for all routes
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

# Add request logging middleware
@app.before_request
def log_request_info():
    if app.debug:
        print(f"Request: {request.method} {request.url}")
        if request.is_json:
            print(f"JSON: {request.get_json()}")

# Add response headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Cleanup function for graceful shutdown
def cleanup():
    """Cleanup function called on application shutdown"""
    try:
        # Close any open database connections
        if hasattr(g, 'db') and g.db:
            g.db.close()
        print("Application cleanup completed")
    except Exception as e:
        print(f"Cleanup error: {e}")









# Add API endpoints
@app.route('/api/ww2/events', methods=['GET'])
def get_ww2_events():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        db = get_db()
        cursor = db.cursor()
        
        query = 'SELECT * FROM ww2_events'
        params = []
        
        if start_date and end_date:
            query += ' WHERE date BETWEEN ? AND ?'
            params = [start_date, end_date]
        
        query += ' ORDER BY date'
        
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        return jsonify([dict(event) for event in events])
        
    except Exception as e:
        print(f"Get WW2 events error: {e}")
        return jsonify({'message': 'Failed to fetch events'}), 500

@app.route('/api/ww2/frontlines', methods=['GET'])
def get_ww2_frontlines():
    try:
        date = request.args.get('date')
        theater = request.args.get('theater')
        
        db = get_db()
        cursor = db.cursor()
        
        if date:
            # Get the closest front line to the specified date
            cursor.execute('''
                SELECT * FROM ww2_frontlines 
                WHERE date <= ? AND (? IS NULL OR theater = ?)
                ORDER BY date DESC 
                LIMIT 1
            ''', (date, theater, theater))
        else:
            cursor.execute('''
                SELECT * FROM ww2_frontlines 
                WHERE ? IS NULL OR theater = ?
                ORDER BY date
            ''', (theater, theater))
        
        frontlines = cursor.fetchall()
        
        # Parse coordinates JSON
        result = []
        for frontline in frontlines:
            frontline_dict = dict(frontline)
            frontline_dict['coordinates'] = json.loads(frontline_dict['coordinates'])
            result.append(frontline_dict)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get WW2 frontlines error: {e}")
        return jsonify({'message': 'Failed to fetch frontlines'}), 500

@app.route('/api/ww2/timeline', methods=['GET'])
def get_ww2_timeline():
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get unique dates from both events and frontlines
        cursor.execute('''
            SELECT DISTINCT date FROM (
                SELECT date FROM ww2_events
                UNION
                SELECT date FROM ww2_frontlines
            ) ORDER BY date
        ''')
        
        dates = [row['date'] for row in cursor.fetchall()]
        
        return jsonify(dates)
        
    except Exception as e:
        print(f"Get WW2 timeline error: {e}")
        return jsonify({'message': 'Failed to fetch timeline'}), 500
def init_veterans_data():
    """Initialize veterans and positions data"""
    db = get_db()
    cursor = db.cursor()
    
    # Create veterans table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veterans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_date TEXT,
            death_date TEXT,
            photo_path TEXT,
            biography TEXT,
            position_id INTEGER,
            unit TEXT,
            awards TEXT,
            battles TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (position_id) REFERENCES military_positions (id)
        )
    ''')
    
    # Create military positions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS military_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            rank_level INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert military positions
    positions = [
        ('Рядовой', 1),
        ('Ефрейтор', 2),
        ('Младший сержант', 3),
        ('Сержант', 4),
        ('Старший сержант', 5),
        ('Старшина', 6),
        ('Прапорщик', 7),
        ('Старший прапорщик', 8),
        ('Младший лейтенант', 9),
        ('Лейтенант', 10),
        ('Старший лейтенант', 11),
        ('Капитан', 12),
        ('Майор', 13),
        ('Подполковник', 14),
        ('Полковник', 15),
        ('Генерал-майор', 16),
        ('Генерал-лейтенант', 17),
        ('Генерал-полковник', 18),
        ('Генерал армии', 19),
        ('Маршал', 20)
    ]
    
    for position_name, rank_level in positions:
        cursor.execute('''
            INSERT OR IGNORE INTO military_positions (name, rank_level) 
            VALUES (?, ?)
        ''', (position_name, rank_level))
    
    # Insert sample veterans
    sample_veterans = [
        ('Иванов Иван Иванович', '1920-05-15', '1943-08-23', None, 
         'Участник Сталинградской битвы. Героически погиб при обороне города.', 
         4, '62-я армия', 'Орден Красной Звезды', 'Сталинградская битва'),
        ('Петров Петр Петрович', '1918-12-03', '1945-05-09', None,
         'Прошел путь от Москвы до Берлина. Участник штурма Рейхстага.',
         12, '3-я ударная армия', 'Орден Отечественной войны I степени, Медаль "За взятие Берлина"',
         'Битва за Москву, Штурм Берлина'),
        ('Сидоров Алексей Николаевич', '1922-01-20', '1944-06-15', None,
         'Танкист, участник операции "Багратион". Погиб в боях за освобождение Белоруссии.',
         10, '1-й гвардейский танковый корпус', 'Орден Красного Знамени',
         'Операция "Багратион"'),
    ]
    
    for veteran_data in sample_veterans:
        cursor.execute('''
            INSERT OR IGNORE INTO veterans 
            (full_name, birth_date, death_date, photo_path, biography, position_id, unit, awards, battles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', veteran_data)
    
    db.commit()
def init_db():
    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            avatar TEXT,
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            email_notifications BOOLEAN DEFAULT 1,
            push_notifications BOOLEAN DEFAULT 0,
            public_profile BOOLEAN DEFAULT 1,
            show_email BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            image_path TEXT,
            video_path TEXT,
            category_id INTEGER,
            author_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            views INTEGER DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recording_tags (
            recording_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (recording_id, tag_id),
            FOREIGN KEY (recording_id) REFERENCES recordings (id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
        )
    ''')
    
    # Insert default categories
    default_categories = [
        "Учебная деятельность",
        "Научная деятельность", 
        "Служебная деятельность",
        "Работа с личным составом",
        "Спортивная деятельность"
    ]
    
    for cat_name in default_categories:
        cursor.execute('SELECT id FROM categories WHERE name = ?', (cat_name,))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (cat_name,))
    
    # Insert default tags
    for tag_name in default_categories:
        cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
    
    # Create default admin user
    cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        admin_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role) 
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@faculty.edu', admin_password, 'admin'))
        
        admin_id = cursor.lastrowid
        
        # Create default settings for admin
        cursor.execute('''
            INSERT INTO user_settings (user_id) VALUES (?)
        ''', (admin_id,))
    
    db.commit()
    db.close()

# Initialize database on startup
def create_tables():
    init_db()
    init_ww2_data()
    init_veterans_data()

with app.app_context():
    create_tables()

# Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'message': 'All fields are required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 400
        
        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            return jsonify({'message': 'Email already exists'}), 400
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash) 
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        
        user_id = cursor.lastrowid
        
        # Create default user settings
        cursor.execute('''
            INSERT INTO user_settings (user_id) VALUES (?)
        ''', (user_id,))
        
        db.commit()
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'message': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            if not user['is_active']:
                return jsonify({'message': 'Account is deactivated'}), 403
            
            # Update last login
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
            db.commit()
            
            # Convert user ID to string for JWT subject
            user_id_str = str(user['id'])
            access_token = create_access_token(identity=user_id_str)
            
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'bio': user['bio'],
                'avatar': user['avatar'],
                'created_at': user['created_at']
            }
            
            return jsonify({
                'access_token': access_token,
                'user': user_data
            })
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'message': 'Login failed'}), 500
@app.route('/api/veterans', methods=['GET'])
def get_veterans():
    try:
        db = get_db()
        cursor = db.cursor()
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search', '').strip()
        
        query = '''
            SELECT v.*, mp.name as position_name, mp.rank_level
            FROM veterans v
            LEFT JOIN military_positions mp ON v.position_id = mp.id
        '''
        params = []
        
        if search:
            query += ' WHERE v.full_name LIKE ? OR v.unit LIKE ?'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY v.full_name'
        
        # Get total count
        count_query = 'SELECT COUNT(*) as total FROM veterans v'
        if search:
            count_query += ' WHERE v.full_name LIKE ? OR v.unit LIKE ?'
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # Add pagination
        offset = (page - 1) * per_page
        query += f' LIMIT {per_page} OFFSET {offset}'
        
        cursor.execute(query, params)
        veterans = cursor.fetchall()
        
        result = []
        for veteran in veterans:
            result.append({
                'id': veteran['id'],
                'full_name': veteran['full_name'],
                'birth_date': veteran['birth_date'],
                'death_date': veteran['death_date'],
                'photo_path': veteran['photo_path'],
                'biography': veteran['biography'],
                'position': {
                    'id': veteran['position_id'],
                    'name': veteran['position_name'],
                    'rank_level': veteran['rank_level']
                } if veteran['position_id'] else None,
                'unit': veteran['unit'],
                'awards': veteran['awards'],
                'battles': veteran['battles'],
                'created_at': veteran['created_at']
            })
        
        return jsonify({
            'veterans': result,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
        
    except Exception as e:
        print(f"Get veterans error: {e}")
        return jsonify({'message': 'Failed to fetch veterans'}), 500

@app.route('/api/veterans/<int:veteran_id>', methods=['GET'])
def get_veteran(veteran_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT v.*, mp.name as position_name, mp.rank_level
            FROM veterans v
            LEFT JOIN military_positions mp ON v.position_id = mp.id
            WHERE v.id = ?
        ''', (veteran_id,))
        
        veteran = cursor.fetchone()
        
        if not veteran:
            return jsonify({'message': 'Veteran not found'}), 404
        
        result = {
            'id': veteran['id'],
            'full_name': veteran['full_name'],
            'birth_date': veteran['birth_date'],
            'death_date': veteran['death_date'],
            'photo_path': veteran['photo_path'],
            'biography': veteran['biography'],
            'position': {
                'id': veteran['position_id'],
                'name': veteran['position_name'],
                'rank_level': veteran['rank_level']
            } if veteran['position_id'] else None,
            'unit': veteran['unit'],
            'awards': veteran['awards'],
            'battles': veteran['battles'],
            'created_at': veteran['created_at']
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get veteran error: {e}")
        return jsonify({'message': 'Failed to fetch veteran'}), 500

@app.route('/api/veterans/create', methods=['POST'])
@jwt_required()
def create_veteran():
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Handle form data
        full_name = request.form.get('full_name')
        birth_date = request.form.get('birth_date')
        death_date = request.form.get('death_date')
        biography = request.form.get('biography', '')
        position_id = request.form.get('position_id')
        unit = request.form.get('unit', '')
        awards = request.form.get('awards', '')
        battles = request.form.get('battles', '')
        
        if not full_name:
            return jsonify({'message': 'Full name is required'}), 400
        
        # Handle photo upload
        photo_path = None
        if 'photo' in request.files:
            photo_file = request.files['photo']
            if photo_file and photo_file.filename:
                filename = secure_filename(photo_file.filename)
                filename = f"veteran_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo_file.save(file_path)
                photo_path = f"/uploads/{filename}"
        
        # Insert veteran
        cursor.execute('''
            INSERT INTO veterans 
            (full_name, birth_date, death_date, photo_path, biography, position_id, unit, awards, battles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (full_name, birth_date, death_date, photo_path, biography, 
              position_id if position_id else None, unit, awards, battles))
        
        veteran_id = cursor.lastrowid
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (current_user_id, 'create', f'Добавлен ветеран: {full_name}', 
              f'Создана запись о ветеране: {full_name}'))
        
        db.commit()
        return jsonify({'message': 'Veteran created successfully', 'id': veteran_id}), 201
        
    except Exception as e:
        print(f"Create veteran error: {e}")
        return jsonify({'message': 'Failed to create veteran'}), 500

@app.route('/api/veterans/<int:veteran_id>/update', methods=['PUT'])
@jwt_required()
def update_veteran(veteran_id):
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        full_name = data.get('full_name')
        birth_date = data.get('birth_date')
        death_date = data.get('death_date')
        biography = data.get('biography', '')
        position_id = data.get('position_id')
        unit = data.get('unit', '')
        awards = data.get('awards', '')
        battles = data.get('battles', '')
        
        if not full_name:
            return jsonify({'message': 'Full name is required'}), 400
        
        cursor.execute('''
            UPDATE veterans 
            SET full_name = ?, birth_date = ?, death_date = ?, biography = ?, 
                position_id = ?, unit = ?, awards = ?, battles = ?
            WHERE id = ?
        ''', (full_name, birth_date, death_date, biography, 
              position_id if position_id else None, unit, awards, battles, veteran_id))
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (current_user_id, 'update', f'Обновлен ветеран: {full_name}', 
              f'Обновлена запись о ветеране: {full_name}'))
        
        db.commit()
        return jsonify({'message': 'Veteran updated successfully'})
        
    except Exception as e:
        print(f"Update veteran error: {e}")
        return jsonify({'message': 'Failed to update veteran'}), 500

@app.route('/api/veterans/<int:veteran_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_veteran(veteran_id):
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Get veteran info for cleanup
        cursor.execute('SELECT full_name, photo_path FROM veterans WHERE id = ?', (veteran_id,))
        veteran = cursor.fetchone()
        
        if not veteran:
            return jsonify({'message': 'Veteran not found'}), 404
        
        # Delete photo file if exists
        if veteran['photo_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(veteran['photo_path']))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete veteran
        cursor.execute('DELETE FROM veterans WHERE id = ?', (veteran_id,))
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)   ''', (current_user_id, 'delete', f'Удален ветеран: {veteran["full_name"]}', 
              f'Удалена запись о ветеране: {veteran["full_name"]}'))
        
        db.commit()
        return jsonify({'message': 'Veteran deleted successfully'})
        
    except Exception as e:
        print(f"Delete veteran error: {e}")
        return jsonify({'message': 'Failed to delete veteran'}), 500

@app.route('/api/military-positions', methods=['GET'])
def get_military_positions():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM military_positions ORDER BY rank_level')
        positions = [dict(row) for row in cursor.fetchall()]
        return jsonify(positions)
    except Exception as e:
        print(f"Get military positions error: {e}")
        return jsonify({'message': 'Failed to fetch military positions'}), 500

@app.route('/api/memory-pages/stats', methods=['GET'])
def get_memory_pages_stats():
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get veterans count
        cursor.execute('SELECT COUNT(*) as count FROM veterans')
        veterans_count = cursor.fetchone()['count']
        
        # Get events count
        cursor.execute('SELECT COUNT(*) as count FROM ww2_events')
        events_count = cursor.fetchone()['count']
        
        # Get battles count (unique battles from veterans)
        cursor.execute('SELECT COUNT(DISTINCT battles) as count FROM veterans WHERE battles IS NOT NULL AND battles != ""')
        battles_count = cursor.fetchone()['count']
        
        # Get units count (unique units from veterans)
        cursor.execute('SELECT COUNT(DISTINCT unit) as count FROM veterans WHERE unit IS NOT NULL AND unit != ""')
        units_count = cursor.fetchone()['count']
        
        stats = {
            'veterans': veterans_count,
            'events': events_count,
            'battles': battles_count,
            'units': units_count
        }
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"Get memory pages stats error: {e}")
        return jsonify({'message': 'Failed to fetch stats'}), 500
# User Profile Routes
@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT u.*, s.public_profile, s.show_email 
            FROM users u
            LEFT JOIN user_settings s ON u.id = s.user_id
            WHERE u.id = ? AND u.is_active = 1
        ''', (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        current_user_id = int(get_jwt_identity())
        
        # Check if profile is public or if it's the user's own profile
        if not user['public_profile'] and current_user_id != user_id:
            return jsonify({'message': 'Profile is private'}), 403
        
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'] if (user['show_email'] or current_user_id == user_id) else None,
            'role': user['role'],
            'bio': user['bio'],
            'avatar': user['avatar'],
            'created_at': user['created_at']
        }
        
        return jsonify(user_data)
        
    except Exception as e:
        print(f"Get user profile error: {e}")
        return jsonify({'message': 'Failed to fetch user profile'}), 500

@app.route('/api/users/<int:user_id>/stats', methods=['GET'])
@jwt_required()
def get_user_stats(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get recordings count
        cursor.execute('SELECT COUNT(*) as count FROM recordings WHERE author_id = ?', (user_id,))
        recordings_count = cursor.fetchone()['count']
        
        # Get total views
        cursor.execute('SELECT SUM(views) as total_views FROM recordings WHERE author_id = ?', (user_id,))
        total_views = cursor.fetchone()['total_views'] or 0
        
        # Get activity count (placeholder for likes and rating)
        cursor.execute('SELECT COUNT(*) as activity_count FROM user_activity WHERE user_id = ?', (user_id,))
        activity_count = cursor.fetchone()['activity_count']
        
        stats = {
            'recordings': recordings_count,
            'total_views': total_views,
            'likes': 0,  # Placeholder - implement likes system later
            'rating': activity_count  # Using activity count as rating for now
        }
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"Get user stats error: {e}")
        return jsonify({'message': 'Failed to fetch user stats'}), 500

@app.route('/api/users/<int:user_id>/recordings', methods=['GET'])
@jwt_required()
def get_user_recordings(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT r.*, c.name as category_name, u.username as author_username
            FROM recordings r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.author_id = u.id
            WHERE r.author_id = ?
            ORDER BY r.created_at DESC
        ''', (user_id,))
        
        recordings = cursor.fetchall()
        
        result = []
        for recording in recordings:
            # Get tags for each recording
            cursor.execute('''
                SELECT t.id, t.name FROM tags t
                JOIN recording_tags rt ON t.id = rt.tag_id
                WHERE rt.recording_id = ?
            ''', (recording['id'],))
            tags = cursor.fetchall()
            
            result.append({
                'id': recording['id'],
                'title': recording['title'],
                'content': recording['content'],
                'image_path': recording['image_path'],
                'video_path': recording['video_path'],
                'category': {
                    'id': recording['category_id'],
                    'name': recording['category_name']
                } if recording['category_id'] else None,
                'author': {
                    'id': recording['author_id'],
                    'username': recording['author_username']
                },
                'tags': [{'id': tag['id'], 'name': tag['name']} for tag in tags],
                'created_at': recording['created_at'],
                'updated_at': recording['updated_at'],
                'views': recording['views']
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get user recordings error: {e}")
        return jsonify({'message': 'Failed to fetch user recordings'}), 500

@app.route('/api/users/<int:user_id>/activity', methods=['GET'])
@jwt_required()
def get_user_activity(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT * FROM user_activity 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 50
        ''', (user_id,))
        
        activities = cursor.fetchall()
        
        result = []
        for activity in activities:
            result.append({
                'id': activity['id'],
                'type': activity['type'],
                'title': activity['title'],
                'description': activity['description'],
                'created_at': activity['created_at']
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get user activity error: {e}")
        return jsonify({'message': 'Failed to fetch user activity'}), 500

@app.route('/api/user/settings', methods=['GET'])
@jwt_required()
def get_user_settings():
    try:
        current_user_id = int(get_jwt_identity())
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM user_settings WHERE user_id = ?', (current_user_id,))
        settings = cursor.fetchone()
        
        if not settings:
            # Create default settings
            cursor.execute('''
                INSERT INTO user_settings (user_id) VALUES (?)
            ''', (current_user_id,))
            db.commit()
            
            settings = {
                'email_notifications': True,
                'push_notifications': False,
                'public_profile': True,
                'show_email': False
            }
        else:
            settings = {
                'email_notifications': bool(settings['email_notifications']),
                'push_notifications': bool(settings['push_notifications']),
                'public_profile': bool(settings['public_profile']),
                'show_email': bool(settings['show_email'])
            }
        
        return jsonify(settings)
        
    except Exception as e:
        print(f"Get user settings error: {e}")
        return jsonify({'message': 'Failed to fetch user settings'}), 500

@app.route('/api/user/settings', methods=['PUT'])
@jwt_required()
def update_user_settings():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE user_settings 
            SET email_notifications = ?, push_notifications = ?, 
                public_profile = ?, show_email = ?
            WHERE user_id = ?
        ''', (
            data.get('emailNotifications', True),
            data.get('pushNotifications', False),
            data.get('publicProfile', True),
            data.get('showEmail', False),
            current_user_id
        ))
        
        db.commit()
        return jsonify({'message': 'Settings updated successfully'})
        
    except Exception as e:
        print(f"Update user settings error: {e}")
        return jsonify({'message': 'Failed to update user settings'}), 500

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        bio = data.get('bio', '').strip()
        
        if not username or not email:
            return jsonify({'message': 'Username and email are required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if username is taken by another user
        cursor.execute('SELECT id FROM users WHERE username = ? AND id != ?', (username, current_user_id))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 400
        
        # Check if email is taken by another user
        cursor.execute('SELECT id FROM users WHERE email = ? AND id != ?', (email, current_user_id))
        if cursor.fetchone():
            return jsonify({'message': 'Email already exists'}), 400
        
        cursor.execute('''
            UPDATE users 
            SET username = ?, email = ?, bio = ?
            WHERE id = ?
        ''', (username, email, bio, current_user_id))
        
        db.commit()
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (current_user_id, 'update', 'Профиль обновлен', 'Пользователь обновил свой профиль'))
        
        db.commit()
        
        return jsonify({'message': 'Profile updated successfully'})
        
    except Exception as e:
        print(f"Update user profile error: {e}")
        return jsonify({'message': 'Failed to update profile'}), 500

@app.route('/api/user/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        
        if not current_password or not new_password:
            return jsonify({'message': 'Current and new passwords are required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'message': 'New password must be at least 6 characters long'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # Verify current password
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], current_password):
            return jsonify({'message': 'Current password is incorrect'}), 400
        
        # Update password
        new_password_hash = generate_password_hash(new_password)
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_password_hash, current_user_id))
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (current_user_id, 'update', 'Пароль изменен', 'Пользователь изменил свой пароль'))
        
        db.commit()
        
        return jsonify({'message': 'Password changed successfully'})
        
    except Exception as e:
        print(f"Change password error: {e}")
        return jsonify({'message': 'Failed to change password'}), 500

@app.route('/api/user/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    try:
        current_user_id = int(get_jwt_identity())
        
        if 'avatar' not in request.files:
            return jsonify({'message': 'No avatar file provided'}), 400
        
        file = request.files['avatar']
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        if file and file.filename:
            filename = secure_filename(file.filename)
            filename = f"avatar_{current_user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            avatar_url = f"/uploads/{filename}"
            
            db = get_db()
            cursor = db.cursor()
            
            # Remove old avatar file if exists
            cursor.execute('SELECT avatar FROM users WHERE id = ?', (current_user_id,))
            old_avatar = cursor.fetchone()
            if old_avatar and old_avatar['avatar']:
                old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(old_avatar['avatar']))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            # Update user avatar
            cursor.execute('UPDATE users SET avatar = ? WHERE id = ?', (avatar_url, current_user_id))
            
            # Log activity
            cursor.execute('''
                INSERT INTO user_activity (user_id, type, title, description)
                VALUES (?, ?, ?, ?)
            ''', (current_user_id, 'update', 'Аватар обновлен', 'Пользователь загрузил новый аватар'))
            
            db.commit()
            
            return jsonify({'message': 'Avatar uploaded successfully', 'avatar_url': avatar_url})
        
    except Exception as e:
        print(f"Upload avatar error: {e}")
        return jsonify({'message': 'Failed to upload avatar'}), 500

# Recording Routes - Separate GET and POST

# GET all recordings
@app.route('/api/recordings', methods=['GET'])
def get_recordings():
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build base query
        query = '''
            SELECT r.*, c.name as category_name, u.username as author_username
            FROM recordings r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.author_id = u.id
        '''
        params = []
        conditions = []
        
        # Add search condition
        if search:
            conditions.append('(r.title LIKE ? OR r.content LIKE ?)')
            params.extend([f'%{search}%', f'%{search}%'])
        
        # Add category filter
        if category:
            conditions.append('r.category_id = ?')
            params.append(category)
        
        # Add WHERE clause if conditions exist
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        # Add sorting
        valid_sort_fields = ['created_at', 'title', 'updated_at', 'views']
        if sort_by in valid_sort_fields:
            query += f' ORDER BY r.{sort_by}'
            if sort_order.lower() == 'desc':
                query += ' DESC'
            else:
                query += ' ASC'
        else:
            query += ' ORDER BY r.created_at DESC'
        
        # Get total count for pagination
        count_query = 'SELECT COUNT(*) as total FROM recordings r'
        if conditions:
            count_query += ' WHERE ' + ' AND '.join(conditions)
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # Add pagination
        offset = (page - 1) * per_page
        query += f' LIMIT {per_page} OFFSET {offset}'
        
        cursor.execute(query, params)
        recordings = cursor.fetchall()
        
        # Get tags for each recording
        result_recordings = []
        for recording in recordings:
            cursor.execute('''
                SELECT t.id, t.name FROM tags t
                JOIN recording_tags rt ON t.id = rt.tag_id
                WHERE rt.recording_id = ?
            ''', (recording['id'],))
            tags = cursor.fetchall()
            
            result_recordings.append({
                'id': recording['id'],
                'title': recording['title'],
                'content': recording['content'],
                'image_path': recording['image_path'],
                'video_path': recording['video_path'],
                'category': {
                    'id': recording['category_id'], 
                    'name': recording['category_name']
                } if recording['category_id'] else None,
                'author': {
                    'id': recording['author_id'], 
                    'username': recording['author_username']
                } if recording['author_id'] else None,
                'user_id': recording['author_id'],
                'tags': [{'id': tag['id'], 'name': tag['name']} for tag in tags],
                'created_at': recording['created_at'],
                'updated_at': recording['updated_at'],
                'views': recording['views']
            })
        
        return jsonify({
            'recordings': result_recordings,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
        
    except Exception as e:
        print(f"Get recordings error: {e}")
        return jsonify({'message': 'Failed to fetch recordings'}), 500

# POST create new recording
@app.route('/api/recordings/create', methods=["GET",'POST'])
@jwt_required()
def create_recording():
    try:
        current_user_id = get_jwt_identity()
        
                # Ensure current_user_id is a string for JWT
        if isinstance(current_user_id, (int, float)):
            current_user_id = str(current_user_id)
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Handle form data (multipart/form-data)
        title = request.form.get('title')
        content = request.form.get('content', '')
        category_id = request.form.get('category_id')
        tags_json = request.form.get('tags', '[]')
        
        if not title:
            return jsonify({'message': 'Title is required'}), 400
        
        # Parse tags
        try:
            tag_ids = json.loads(tags_json) if tags_json else []
        except json.JSONDecodeError:
            tag_ids = []
        
        # Handle file uploads
        image_path = None
        video_path = None
        
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(file_path)
                image_path = f"/uploads/{filename}"
        
        if 'video' in request.files:
            video_file = request.files['video']
            if video_file and video_file.filename:
                filename = secure_filename(video_file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video_file.save(file_path)
                video_path = f"/uploads/{filename}"
        
        # Insert recording - convert current_user_id back to int for database
        cursor.execute('''
            INSERT INTO recordings (title, content, category_id, author_id, image_path, video_path) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, category_id if category_id else None, int(current_user_id), image_path, video_path))
        
        recording_id = cursor.lastrowid
        
        # Add tags
        if tag_ids:
            for tag_data in tag_ids:
                if isinstance(tag_data, dict):
                    if tag_data.get('isNew'):
                        # Create new tag
                        cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_data['name'],))
                        tag_id = cursor.lastrowid
                    else:
                        tag_id = tag_data['id']
                else:
                    tag_id = tag_data
                
                cursor.execute('''
                    INSERT OR IGNORE INTO recording_tags (recording_id, tag_id) 
                    VALUES (?, ?)
                ''', (recording_id, tag_id))
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (int(current_user_id), 'create', title, f'Создана новая запись: {title}'))
        
        db.commit()
        return jsonify({'message': 'Recording created successfully', 'id': recording_id}), 201
        
    except Exception as e:
        print(f"Create recording error: {e}")
        return jsonify({'message': 'Failed to create recording'}), 500


# GET single recording by ID
@app.route('/api/recordings/<int:recording_id>', methods=['GET'])
def get_recording(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get recording with related data
        cursor.execute('''
            SELECT r.*, c.name as category_name, u.username as author_username
            FROM recordings r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.author_id = u.id
            WHERE r.id = ?
        ''', (recording_id,))
        
        recording = cursor.fetchone()
        
        if not recording:
            return jsonify({'message': 'Recording not found'}), 404
        
        # Get tags for this recording
        cursor.execute('''
            SELECT t.id, t.name FROM tags t
            JOIN recording_tags rt ON t.id = rt.tag_id
            WHERE rt.recording_id = ?
        ''', (recording_id,))
        tags = cursor.fetchall()
        
        # Increment view count
        cursor.execute('UPDATE recordings SET views = views + 1 WHERE id = ?', (recording_id,))
        db.commit()
        
        # Format response
        result = {
            'id': recording['id'],
            'title': recording['title'],
            'content': recording['content'],
            'image_path': recording['image_path'],
            'video_path': recording['video_path'],
            'category': {
                'id': recording['category_id'],
                'name': recording['category_name']
            } if recording['category_id'] else None,
            'user': {
                'id': recording['author_id'],
                'username': recording['author_username']
            } if recording['author_id'] else None,
            'user_id': recording['author_id'],
            'tags': [{'id': tag['id'], 'name': tag['name']} for tag in tags],
            'created_at': recording['created_at'],
            'updated_at': recording['updated_at'],
            'views': recording['views']
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get recording error: {e}")
        return jsonify({'message': 'Failed to fetch recording'}), 500

# PUT update recording
@app.route('/api/recordings/<int:recording_id>/update', methods=['PUT'])
@jwt_required()
def update_recording(recording_id):
    try:
        current_user_id = get_jwt_identity()
        # Convert to int for database operations
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        title = data.get('title')
        content = data.get('content', '')
        category_id = data.get('category_id')
        
        if not title:
            return jsonify({'message': 'Title is required'}), 400
        
        cursor.execute('''
            UPDATE recordings 
            SET title = ?, content = ?, category_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, category_id, recording_id))
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (current_user_id, 'update', title, f'Обновлена запись: {title}'))
        
        db.commit()
        return jsonify({'message': 'Recording updated successfully'})
        
    except Exception as e:
        print(f"Update recording error: {e}")
        return jsonify({'message': 'Failed to update recording'}), 500

@app.route('/api/recordings/<int:recording_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_recording(recording_id):
    try:
        current_user_id = get_jwt_identity()
        # Convert to int for database operations
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Get recording info for cleanup and logging
        cursor.execute('SELECT title, image_path, video_path FROM recordings WHERE id = ?', (recording_id,))
        recording = cursor.fetchone()
        
        if not recording:
            return jsonify({'message': 'Recording not found'}), 404
        
        # Delete associated files
        if recording['image_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['image_path']))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if recording['video_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['video_path']))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete recording tags
        cursor.execute('DELETE FROM recording_tags WHERE recording_id = ?', (recording_id,))
        
        # Delete recording
        cursor.execute('DELETE FROM recordings WHERE id = ?', (recording_id,))
        
        # Log activity
        cursor.execute('''
            INSERT INTO user_activity (user_id, type, title, description)
            VALUES (?, ?, ?, ?)
        ''', (current_user_id, 'delete', recording['title'], f'Удалена запись: {recording["title"]}'))
        
        db.commit()
        return jsonify({'message': 'Recording deleted successfully'})
        
    except Exception as e:
        print(f"Delete recording error: {e}")
        return jsonify({'message': 'Failed to delete recording'}), 500

# GET latest recordings
@app.route('/api/recordings/latest', methods=['GET'])
def get_latest_recordings():
    try:
        db = get_db()
        cursor = db.cursor()
        
        limit = int(request.args.get('limit', 5))
        
        cursor.execute('''
            SELECT r.*, c.name as category_name, u.username as author_username
            FROM recordings r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.author_id = u.id
            ORDER BY r.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        recordings = cursor.fetchall()
        
        result = []
        for recording in recordings:
            # Get tags for each recording
            cursor.execute('''
                SELECT t.id, t.name FROM tags t
                JOIN recording_tags rt ON t.id = rt.tag_id
                WHERE rt.recording_id = ?
            ''', (recording['id'],))
            tags = cursor.fetchall()
            
            result.append({
                'id': recording['id'],
                'title': recording['title'],
                'content': recording['content'],
                'image_path': recording['image_path'],
                'video_path': recording['video_path'],
                'category': {
                    'id': recording['category_id'],
                    'name': recording['category_name']
                } if recording['category_id'] else None,
                'author': {
                    'id': recording['author_id'],
                    'username': recording['author_username']
                } if recording['author_id'] else None,
                'tags': [{'id': tag['id'], 'name': tag['name']} for tag in tags],
                'created_at': recording['created_at'],
                'views': recording['views']
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get latest recordings error: {e}")
        return jsonify({'message': 'Failed to fetch latest recordings'}), 500

# GET related recordings
@app.route('/api/recordings/<int:recording_id>/related', methods=['GET'])
def get_related_recordings(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get current recording's category
        cursor.execute('SELECT category_id FROM recordings WHERE id = ?', (recording_id,))
        current_recording = cursor.fetchone()
        
        if not current_recording:
            return jsonify([])
        
        category_id = current_recording['category_id']
        limit = int(request.args.get('limit', 3))
        
        if category_id:
            # Get recordings from same category
            cursor.execute('''
                SELECT r.*, c.name as category_name, u.username as author_username
                FROM recordings r
                LEFT JOIN categories c ON r.category_id = c.id
                LEFT JOIN users u ON r.author_id = u.id
                WHERE r.category_id = ? AND r.id != ?
                ORDER BY r.created_at DESC
                LIMIT ?
            ''', (category_id, recording_id, limit))
        else:
            # Get latest recordings if no category
            cursor.execute('''
                SELECT r.*, c.name as category_name, u.username as author_username
                FROM recordings r
                LEFT JOIN categories c ON r.category_id = c.id
                LEFT JOIN users u ON r.author_id = u.id
                WHERE r.id != ?
                ORDER BY r.created_at DESC
                LIMIT ?
            ''', (recording_id, limit))
        
        recordings = cursor.fetchall()
        
        result = []
        for recording in recordings:
            result.append({
                'id': recording['id'],
                'title': recording['title'],
                'content': recording['content'],
                'image_path': recording['image_path'],
                'category': {
                    'id': recording['category_id'],
                    'name': recording['category_name']
                } if recording['category_id'] else None,
                'created_at': recording['created_at']
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get related recordings error: {e}")
        return jsonify([])

# Categories Routes
@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM categories ORDER BY name')
        categories = [dict(row) for row in cursor.fetchall()]
        return jsonify(categories)
    except Exception as e:
        print(f"Get categories error: {e}")
        return jsonify({'message': 'Failed to fetch categories'}), 500

@app.route('/api/categories/create', methods=['POST'])
@jwt_required()
def create_category():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'message': 'Category name is required'}), 400
        
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        db.commit()
        
        return jsonify({'message': 'Category created successfully', 'id': cursor.lastrowid}), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Category already exists'}), 400
    except Exception as e:
        print(f"Create category error: {e}")
        return jsonify({'message': 'Failed to create category'}), 500

# Tags Routes
@app.route('/api/tags', methods=['GET'])
def get_tags():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tags ORDER BY name')
        tags = [dict(row) for row in cursor.fetchall()]
        return jsonify(tags)
    except Exception as e:
        print(f"Get tags error: {e}")
        return jsonify({'message': 'Failed to fetch tags'}), 500

@app.route('/api/tags/create', methods=['POST'])
@jwt_required()
def create_tag():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'message': 'Tag name is required'}), 400
        
        cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
        db.commit()
        
        return jsonify({'message': 'Tag created successfully', 'id': cursor.lastrowid}), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Tag already exists'}), 400
    except Exception as e:
        print(f"Create tag error: {e}")
        return jsonify({'message': 'Failed to create tag'}), 500

# File serving route
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file("../"+app.config['UPLOAD_FOLDER']+"/"+filename)

# Admin routes (keeping existing admin functionality)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND role IN ("admin", "moderator")', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['admin_user_id'] = user['id']
            session['admin_username'] = user['username']
            session['admin_role'] = user['role']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()
    cursor = db.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as total FROM users')
    total_users = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM recordings')
    total_recordings = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM users WHERE created_at >= date("now", "-30 days")')
    new_users_month = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM recordings WHERE created_at >= date("now", "-30 days")')
    new_recordings_month = cursor.fetchone()['total']
    
    stats = {
        'total_users': total_users,
        'total_recordings': total_recordings,
        'new_users_month': new_users_month,
        'new_recordings_month': new_recordings_month
    }
    
    # Get recent users
    cursor.execute('''
        SELECT * FROM users 
        ORDER BY created_at DESC 
        LIMIT 5
    ''')
    recent_users = cursor.fetchall()
    
    # Get recent recordings
    cursor.execute('''
        SELECT r.*, u.username as author
        FROM recordings r
        LEFT JOIN users u ON r.author_id = u.id
        ORDER BY r.created_at DESC 
        LIMIT 5
    ''')
    recent_recordings = cursor.fetchall()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_users=recent_users,
                         recent_recordings=recent_recordings)

@app.route('/admin/users')
@admin_required
def admin_users():
    db = get_db()
    cursor = db.cursor()
    
    # Get filters
    search = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Build query
    query = 'SELECT * FROM users'
    params = []
    conditions = []
    
    if search:
        conditions.append('(username LIKE ? OR email LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%'])
    
    if role_filter:
        conditions.append('role = ?')
        params.append(role_filter)
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY created_at DESC'
    
    # Get total count
    count_query = 'SELECT COUNT(*) as total FROM users'
    if conditions:
        count_query += ' WHERE ' + ' AND '.join(conditions)
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    # Add pagination
    offset = (page - 1) * per_page
    query += f' LIMIT {per_page} OFFSET {offset}'
    
    cursor.execute(query, params)
    users = cursor.fetchall()
    
    return render_template('admin/users.html', 
                         users=users, 
                         total=total,
                         search=search,
                         role_filter=role_filter,
                         page=page,
                         per_page=per_page,
                         total_pages=(total + per_page - 1) // per_page)

@app.route('/admin/recordings')
@admin_required
def admin_recordings():
    db = get_db()
    cursor = db.cursor()
    
    # Get filters
    search = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Build query
    query = '''
        SELECT r.*, c.name as category_name, u.username as author_username
        FROM recordings r
        LEFT JOIN categories c ON r.category_id = c.id
        LEFT JOIN users u ON r.author_id = u.id
    '''
    params = []
    conditions = []
    
    if search:
        conditions.append('(r.title LIKE ? OR r.content LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category_filter:
        conditions.append('r.category_id = ?')
        params.append(category_filter)
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY r.created_at DESC'
    
    # Get total count
    count_query = 'SELECT COUNT(*) as total FROM recordings r'
    if conditions:
        count_query += ' WHERE ' + ' AND '.join(conditions)
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    # Add pagination
    offset = (page - 1) * per_page
    query += f' LIMIT {per_page} OFFSET {offset}'
    
    cursor.execute(query, params)
    recordings = cursor.fetchall()
    
    # Get categories for filter
    cursor.execute('SELECT * FROM categories ORDER BY name')
    categories = cursor.fetchall()
    
    return render_template('admin/recordings.html', 
                         recordings=recordings, 
                         categories=categories,
                         total=total,
                         search=search,
                         category_filter=category_filter,
                         page=page,
                         per_page=per_page,
                         total_pages=(total + per_page - 1) // per_page)

@app.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    try:
        # Prevent admin from deactivating themselves
        if user_id == session.get('admin_user_id'):
            flash('You cannot deactivate your own account', 'error')
            return redirect(url_for('admin_users'))
        
        db = get_db()
        cursor = db.cursor()
        
        # Get current status
        cursor.execute('SELECT is_active FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            new_status = not user['is_active']
            cursor.execute('UPDATE users SET is_active = ? WHERE id = ?', (new_status, user_id))
            db.commit()
            
            status_text = 'activated' if new_status else 'deactivated'
            flash(f'User {status_text} successfully', 'success')
        else:
            flash('User not found', 'error')
            
    except Exception as e:
        print(f"Toggle user status error: {e}")
        flash('Failed to update user status', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/recordings/<int:recording_id>/delete', methods=['POST'])
@admin_required
def admin_delete_recording(recording_id):
    db = get_db()
    cursor = db.cursor()
    
    # Get recording info
    cursor.execute('SELECT * FROM recordings WHERE id = ?', (recording_id,))
    recording = cursor.fetchone()
    
    if recording:
        # Delete associated files
        if recording['image_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                   recording['image_path'].replace('/uploads/', ''))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if recording['video_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                   recording['video_path'].replace('/uploads/', ''))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete recording
        cursor.execute('DELETE FROM recordings WHERE id = ?', (recording_id,))
        db.commit()
        
        flash('Recording deleted successfully!', 'success')
    else:
        flash('Recording not found!', 'error')
    
    return redirect(url_for('admin_recordings'))

@app.route('/admin/recordings/<int:recording_id>/details')
@admin_required
def get_recording_details(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT r.*, u.username as author, c.name as category
            FROM recordings r
            LEFT JOIN users u ON r.author_id = u.id
            LEFT JOIN categories c ON r.category_id = c.id
            WHERE r.id = ?
        ''', (recording_id,))
        
        recording = cursor.fetchone()
        
        if not recording:
            return jsonify({'success': False, 'message': 'Recording not found'}), 404
        
        return jsonify({
            'success': True,
            'recording': dict(recording)
        })
        
    except Exception as e:
        print(f"Get recording details error: {e}")
        return jsonify({'success': False, 'message': 'Failed to get recording details'}), 500

@app.route('/admin/recordings/<int:recording_id>/delete', methods=['POST'])
@admin_required
def delete_recording_admin(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get recording info for file cleanup
        cursor.execute('SELECT image_path, video_path FROM recordings WHERE id = ?', (recording_id,))
        recording = cursor.fetchone()
        
        if recording:
            # Delete associated files
            if recording['image_path']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['image_path']))
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            if recording['video_path']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['video_path']))
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Delete recording tags
            cursor.execute('DELETE FROM recording_tags WHERE recording_id = ?', (recording_id,))
            
            # Delete recording
            cursor.execute('DELETE FROM recordings WHERE id = ?', (recording_id,))
            
            db.commit()
            flash('Recording deleted successfully', 'success')
        else:
            flash('Recording not found', 'error')
            
    except Exception as e:
        print(f"Delete recording error: {e}")
        flash('Failed to delete recording', 'error')
    
    return redirect(url_for('admin_recordings'))
# Add these new admin routes after the existing ones

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            role = request.form.get('role', 'user')
            bio = request.form.get('bio', '').strip()
            is_active = bool(request.form.get('is_active'))
            
            if not username or not email:
                flash('Username and email are required', 'error')
                return redirect(url_for('edit_user', user_id=user_id))
            
            # Check if username is taken by another user
            cursor.execute('SELECT id FROM users WHERE username = ? AND id != ?', (username, user_id))
            if cursor.fetchone():
                flash('Username already taken', 'error')
                return redirect(url_for('edit_user', user_id=user_id))
            
            # Check if email is taken by another user
            cursor.execute('SELECT id FROM users WHERE email = ? AND id != ?', (email, user_id))
            if cursor.fetchone():
                flash('Email already taken', 'error')
                return redirect(url_for('edit_user', user_id=user_id))
            
            # Update user
            cursor.execute('''
                UPDATE users 
                SET username = ?, email = ?, role = ?, bio = ?, is_active = ?
                WHERE id = ?
            ''', (username, email, role, bio, is_active, user_id))
            
            db.commit()
            flash('User updated successfully', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            print(f"Edit user error: {e}")
            flash('Failed to update user', 'error')
    
    # GET request - show edit form
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.html', user=user)

@app.route('/admin/users/<int:user_id>/change-password', methods=['POST'])
@admin_required
def admin_change_user_password(user_id):
    try:
        new_password = request.form.get('new_password', '').strip()
        
        if not new_password or len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('edit_user', user_id=user_id))
        
        db = get_db()
        cursor = db.cursor()
        
        # Update password
        password_hash = generate_password_hash(new_password)
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
        db.commit()
        
        flash('Password changed successfully', 'success')
        
    except Exception as e:
        print(f"Admin change password error: {e}")
        flash('Failed to change password', 'error')
    
    return redirect(url_for('edit_user', user_id=user_id))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    try:
        # Prevent admin from deleting themselves
        if user_id == session.get('admin_user_id'):
            flash('You cannot delete your own account', 'error')
            return redirect(url_for('admin_users'))
        
        db = get_db()
        cursor = db.cursor()
        
        # Get user info
        cursor.execute('SELECT username, avatar FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            # Delete user avatar if exists
            if user['avatar']:
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(user['avatar']))
                if os.path.exists(avatar_path):
                    try:
                        os.remove(avatar_path)
                    except:
                        pass
            
            # Delete user's recordings and associated files
            cursor.execute('SELECT image_path, video_path FROM recordings WHERE author_id = ?', (user_id,))
            recordings = cursor.fetchall()
            
            for recording in recordings:
                if recording['image_path']:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['image_path']))
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except:
                            pass
                
                if recording['video_path']:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['video_path']))
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except:
                            pass
            
            # Delete user (cascade will handle related records)
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            db.commit()
            
            flash(f'User "{user["username"]}" deleted successfully', 'success')
        else:
            flash('User not found', 'error')
            
    except Exception as e:
        print(f"Delete user error: {e}")
        flash('Failed to delete user', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/recordings/<int:recording_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_recording(recording_id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            category_id = request.form.get('category_id')
            tag_ids = request.form.getlist('tag_ids')
            
            if not title:
                flash('Title is required', 'error')
                return redirect(url_for('edit_recording', recording_id=recording_id))
            
            # Update recording
            cursor.execute('''
                UPDATE recordings 
                SET title = ?, content = ?, category_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (title, content, category_id if category_id else None, recording_id))
            
            # Update tags - first remove all existing tags
            cursor.execute('DELETE FROM recording_tags WHERE recording_id = ?', (recording_id,))
            
            # Add new tags
            for tag_id in tag_ids:
                if tag_id:
                    cursor.execute('''
                        INSERT INTO recording_tags (recording_id, tag_id) 
                        VALUES (?, ?)
                    ''', (recording_id, int(tag_id)))
            
            # Handle file uploads
            if 'image' in request.files and request.files['image'].filename:
                image_file = request.files['image']
                filename = secure_filename(image_file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(file_path)
                
                # Delete old image
                cursor.execute('SELECT image_path FROM recordings WHERE id = ?', (recording_id,))
                old_image = cursor.fetchone()
                if old_image and old_image['image_path']:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(old_image['image_path']))
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except:
                            pass
                
                cursor.execute('UPDATE recordings SET image_path = ? WHERE id = ?', (f"/uploads/{filename}", recording_id))
            
            if 'video' in request.files and request.files['video'].filename:
                video_file = request.files['video']
                filename = secure_filename(video_file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video_file.save(file_path)
                
                # Delete old video
                cursor.execute('SELECT video_path FROM recordings WHERE id = ?', (recording_id,))
                old_video = cursor.fetchone()
                if old_video and old_video['video_path']:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(old_video['video_path']))
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except:
                            pass
                
                cursor.execute('UPDATE recordings SET video_path = ? WHERE id = ?', (f"/uploads/{filename}", recording_id))
            
            db.commit()
            flash('Recording updated successfully', 'success')
            return redirect(url_for('admin_recordings'))
            
        except Exception as e:
            print(f"Edit recording error: {e}")
            flash('Failed to update recording', 'error')
    
    # GET request - show edit form
    cursor.execute('''
        SELECT r.*, c.name as category_name, u.username as author_username
        FROM recordings r
        LEFT JOIN categories c ON r.category_id = c.id
        LEFT JOIN users u ON r.author_id = u.id
        WHERE r.id = ?
    ''', (recording_id,))
    
    recording = cursor.fetchone()
    
    if not recording:
        flash('Recording not found', 'error')
        return redirect(url_for('admin_recordings'))
    
    # Get recording tags
    cursor.execute('''
        SELECT t.id, t.name FROM tags t
        JOIN recording_tags rt ON t.id = rt.tag_id
        WHERE rt.recording_id = ?
    ''', (recording_id,))
    recording_tags = cursor.fetchall()
    
    # Get all categories and tags
    cursor.execute('SELECT * FROM categories ORDER BY name')
    categories = cursor.fetchall()
    
    cursor.execute('SELECT * FROM tags ORDER BY name')
    tags = cursor.fetchall()
    
    return render_template('admin/edit_recording.html', 
                         recording=recording, 
                         recording_tags=recording_tags,
                         categories=categories, 
                         tags=tags)

@app.route('/admin/tags', methods=['GET'])
@admin_required
def admin_tags():
    db = get_db()
    cursor = db.cursor()
    
    # Get all tags with usage count
    cursor.execute('''
        SELECT t.*, COUNT(rt.recording_id) as usage_count
        FROM tags t
        LEFT JOIN recording_tags rt ON t.id = rt.tag_id
        GROUP BY t.id
        ORDER BY t.name
    ''')
    tags = cursor.fetchall()
    
    return render_template('admin/tags.html', tags=tags)

@app.route('/admin/tags/create', methods=['POST'])
@admin_required
def admin_create_tag():
    try:
        name = request.form.get('name', '').strip()
        
        if not name:
            flash('Tag name is required', 'error')
            return redirect(url_for('admin_tags'))
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
        db.commit()
        
        flash('Tag created successfully', 'success')
        
    except sqlite3.IntegrityError:
        flash('Tag already exists', 'error')
    except Exception as e:
        print(f"Create tag error: {e}")
        flash('Failed to create tag', 'error')
    
    return redirect(url_for('admin_tags'))

@app.route('/admin/tags/<int:tag_id>/edit', methods=['POST'])
@admin_required
def admin_edit_tag(tag_id):
    try:
        name = request.form.get('name', '').strip()
        
        if not name:
            flash('Tag name is required', 'error')
            return redirect(url_for('admin_tags'))
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('UPDATE tags SET name = ? WHERE id = ?', (name, tag_id))
        db.commit()
        
        flash('Tag updated successfully', 'success')
        
    except sqlite3.IntegrityError:
        flash('Tag name already exists', 'error')
    except Exception as e:
        print(f"Edit tag error: {e}")
        flash('Failed to update tag', 'error')
    
    return redirect(url_for('admin_tags'))

@app.route('/admin/tags/<int:tag_id>/delete', methods=['POST'])
@admin_required
def admin_delete_tag(tag_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get tag name for confirmation
        cursor.execute('SELECT name FROM tags WHERE id = ?', (tag_id,))
        tag = cursor.fetchone()
        
        if tag:
            # Delete tag (cascade will handle recording_tags)
            cursor.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
            db.commit()
            
            flash(f'Tag "{tag["name"]}" deleted successfully', 'success')
        else:
            flash('Tag not found', 'error')
            
    except Exception as e:
        print(f"Delete tag error: {e}")
        flash('Failed to delete tag', 'error')
    
    return redirect(url_for('admin_tags'))

@app.route('/admin/categories', methods=['GET'])
@admin_required
def admin_categories():
    db = get_db()
    cursor = db.cursor()
    
    # Get all categories with usage count
    cursor.execute('''
        SELECT c.*, COUNT(r.id) as usage_count
        FROM categories c
        LEFT JOIN recordings r ON c.id = r.category_id
        GROUP BY c.id
        ORDER BY c.name
    ''')
    categories = cursor.fetchall()
    
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/create', methods=['POST'])
@admin_required
def admin_create_category():
    try:
        name = request.form.get('name', '').strip()
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('admin_categories'))
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        db.commit()
        
        flash('Category created successfully', 'success')
        
    except sqlite3.IntegrityError:
        flash('Category already exists', 'error')
    except Exception as e:
        print(f"Create category error: {e}")
        flash('Failed to create category', 'error')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/<int:category_id>/edit', methods=['POST'])
@admin_required
def admin_edit_category(category_id):
    try:
        name = request.form.get('name', '').strip()
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('admin_categories'))
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
        db.commit()
        
        flash('Category updated successfully', 'success')
        
    except sqlite3.IntegrityError:
        flash('Category name already exists', 'error')
    except Exception as e:
        print(f"Edit category error: {e}")
        flash('Failed to update category', 'error')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if category is in use
        cursor.execute('SELECT COUNT(*) as count FROM recordings WHERE category_id = ?', (category_id,))
        usage_count = cursor.fetchone()['count']
        
        if usage_count > 0:
            flash(f'Cannot delete category. It is used by {usage_count} recording(s)', 'error')
            return redirect(url_for('admin_categories'))
        
        # Get category name for confirmation
        cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        
        if category:
            cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            db.commit()
            
            flash(f'Category "{category["name"]}" deleted successfully', 'success')
        else:
            flash('Category not found', 'error')
            
    except Exception as e:
        print(f"Delete category error: {e}")
        flash('Failed to delete category', 'error')
    
    return redirect(url_for('admin_categories'))


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

