using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SQLiteDemo
{
    class Program
    {

        static void Main(string[] args)
        {
            SQLiteConnection sqlite_conn;
            sqlite_conn = CreateConnection();
            Console.WriteLine("Testing");
            //CreateTable(sqlite_conn);
            ResponseParser parser;
            parser.ParseCSV("Call Center Form.csv");
            foreach (var ev in parser.Events) {
                string sqlite_id_cmd = $"INSERT INTO Case(CaseID) VALUES({ev.GetID()});";
                int[] tags = ev.GetCategories();
                string sqlite_tags_cmd = $"INSERT INTO Tags VALUES({tags[0]},{tags[1]},{tags[3]},{tags[4]},{tags[5]},{ev.GetID()});";
                string sqlite_desc_cmd = $"INSERT INTO Description VALUES({ev.GetID()},{ev.GetName},{ev.GetDescription});";

                
                InsertData(sqlite_conn, sqlite_id_cmd);
                InsertData(sqlite_conn, sqlite_tags_cmd);
                InsertData(sqlite_conn, sqlite_desc_cmd);
            }

            //InsertData(sqlite_conn);
            //ReadData(sqlite_conn);
            
        }

        static SQLiteConnection CreateConnection()
        {

            SQLiteConnection sqlite_conn;
            // Create a new database connection:
            sqlite_conn = new SQLiteConnection("Data Source=Mission.db; Version = 3; New = False; Compress = True; ");
            Console.WriteLine("Opened and connected");
            // Open the connection:
            try
            {
                sqlite_conn.Open();
            }
            catch (Exception ex)
            {

            }
            return sqlite_conn;
        }
        
       static void CreateTable(SQLiteConnection conn)
        {

            SQLiteCommand sqlite_cmd;
            string Createsql = "CREATE TABLE Description(CaseID INT, Name TEXT, Desc BLOB)";
            sqlite_cmd = conn.CreateCommand();
            sqlite_cmd.CommandText = Createsql;
            sqlite_cmd.ExecuteNonQuery();

            Console.WriteLine("Create table command");
        }
        
       static void InsertData(SQLiteConnection conn, string CommandString)
        {
           SQLiteCommand sqlite_cmd;
           sqlite_cmd = conn.CreateCommand();
           sqlite_cmd.CommandText = CommandString;
           sqlite_cmd.ExecuteNonQuery();

            Console.WriteLine("Command Completed");
        }

        
        static void ReadData(SQLiteConnection conn, string CommandString)
        {
            SQLiteDataReader sqlite_datareader;
            SQLiteCommand sqlite_cmd;
            sqlite_cmd = conn.CreateCommand();
            sqlite_cmd.CommandText = CommandString;

            sqlite_datareader = sqlite_cmd.ExecuteReader();
            while (sqlite_datareader.Read())
            {
                string myreader = sqlite_datareader.GetString(0);
                Console.WriteLine(myreader);
            }
            conn.Close();
        }
    } 
}