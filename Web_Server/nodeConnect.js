var express = require('express');
const path = require('path');
var bodyParser = require('body-parser');
var app = express();
const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('Mission.db', sqlite3.OPEN_READWRITE, (err) => {
	if (err) {
		return console.error(err.message);
	}
	debug('Connected to the in-memory SQlite database.');
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var res1;

app.get("/", function (req, res) {
	res1 = res;
	res.sendFile(path.join(__dirname+'/website.html'));
	debug("Entry Site Loaded");
});

app.get("/loginNormal", function (req, res) {
	res1.sendFile(path.join(__dirname+'/homepage.html'));
	debug("Homepage Loaded");
});

app.post("/login", function (req, res) {
	var name = req.body.name;
	var pass = req.body.pass;
	
	db.serialize(() => {
		var query = 'SELECT * FROM Personnel WHERE UserName == "' + name + '" AND Password == "' + pass + '"';
		db.get(query, (err, row) => {
			if (err) {
				console.error(err.message);
			}
			if(row) {
				debug("Account [NAME]: " + name + " [PASSWORD]: " + pass + " | Exists in Database...");
				query = "SELECT * FROM Skills WHERE Skills.ResponderID == " + row.ResponderID;
				db.get(query, (err1, row1) => {
					if(err1) {
						console.error(err1.message);
					}
					var skills = [];
					if(row1.Animal == 1) {
						skills.push(" Animal");
					}
					if(row1.Fire == 1) {
						skills.push(" Fire");
					}
					if(row1.Flood == 1) {
						skills.push(" Flood");
					}
					if(row1.Medical == 1) {
						skills.push(" Medical");
					}
					if(row1.Other != null) {
						skills.push(" [Other: " + row1.Other + "]");
					}
					debug("[SKILLS]:" + skills.toString());
					res.send("Welcome " + name + "... Logging you in...");
					
				});
			}
			else {
				debug("Account [NAME]: " + name + " [PASSWORD]: " + pass + " | Not in Database...");
				//Failed login...
				res.send("Account Does Not Exist!!!");
			}
		});
	});
});

app.post("/newAccount", function (req, res) {
	var name = req.body.name;
	var pass = req.body.pass;
	debug("New Account Info: " + name + " " + pass);
	db.serialize(() => {
		// insert one row into the langs table
		query = 'INSERT INTO Personnel VALUES("' + name + '", "' + pass + '", 2)';
		db.run(query, function(err) {
			if (err) {
				return console.error(err.message);
			}
			// get the last insert amount
			console.log("A row has been inserted " + this);
		});	
	});
});

var server = app.listen("8080")
console.log('Server running port 8080/');

function debug(debugInfo) {
	console.log("[DEBUG]: " + debugInfo);
}