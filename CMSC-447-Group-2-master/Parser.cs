using System;
using System.IO;
using System.Collections.Generic;


namespace ResponseParser
{
    public class CSVParser
    {
        private string path;
        List<Event> Events = new List<Event>();
        int nextID;

        void ParseCSV(string _path)
        {
            path = _path;
            using (StreamReader sr = File.OpenText(path))
            {
                string line;
                string[] lineParts;
                int lineCounter = 0;
                int lineIndex = 0;


                while ((line = sr.ReadLine()) != null)
                {
                    if (lineCounter == 0)
                    {
                        lineCounter++;
                        continue;
                    }
                    string Desc = "";
                    string name = "";
                    string location = "";
                    string date = "";
                    
                    int[] cats = new int[6];
                    foreach (int i in cats)
                    {
                        cats[i] = 0;
                    }

                    lineParts = line.Split(',');
                    int ID = nextID++;
                    foreach (var part in lineParts)
                    {
                        lineIndex++;
                        switch(lineIndex)
                        {
                            case 1:  date = part;
                                break;
                            case 2: name = part;
                                break;
                            case 3: location = part;
                                break;
                           
                            default:
                                if(part[0] == '"')
                                {
                                    part.Remove(0, 1);
                                }
                                if (part[part.Length-1] == '"')
                                {
                                    part.Remove(part.Length - 1);
                                }
                                switch (part)
                                {
                                    case "Animal Support":
                                        cats[0] = 1;
                                        break;
                                    case "Fire":
                                        cats[1] = 1;
                                        break;
                                    case "Electrical":
                                        cats[2] = 1;
                                        break;
                                    case "Flood":
                                        cats[3] = 1;
                                        break;
                                    case "Medical Emergency (Human)":
                                        cats[4] = 1;
                                        break;
                                    case "Other":
                                        cats[5] = 1;
                                        break;
                                    default:
                                        Desc = part;
                                        break;
                                }
                                break;
                        }
                        

                        

                    }
                    Events.Add(new Event(ID, date, name, location, cats, Desc));


                }
            }
        }

        private void UpdateDatabase(List<Event> events)
        {

        }
    }
}
