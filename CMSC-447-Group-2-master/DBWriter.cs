using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResponseParser
{
    class DBWriter
    {
        private void Connect(string _user, string _pass, string _db)
        {
            SqlConnection con = new SqlConnection("user id = user;"
                                                    + "password = 123;"
                                                    + "database = Mission.db;"
                                                    + "connection timeout = 20");

            try
            {
                con.Open();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }

            SqlCommand insertEvent = new SqlCommand("INSERT INTO ");
        }

    }
}
