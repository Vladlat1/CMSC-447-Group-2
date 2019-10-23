using System;
using System.Collections.Generic;
using System.Text;

namespace ResponseParser
{

    public class Event
    {
        private readonly int ID;
        private readonly string Name;
        private readonly string Location;
        private readonly int[] Categories;
        private readonly string Description;
        private readonly string Date;

        public Event(int _ID, string _Date, string _Name, string _Location, int[] _Categories, string _Description)
        {
            ID = _ID;
            Name = _Name;
            Location = _Location;
            Categories = _Categories;
            Description = _Description;
            Date = _Date;
        }

       public int GetID()
        {
            return ID;
        }

        public string GetName()
        {
            return Name;
        }

        public string GetLocation()
        {
            return Location;
        }

        public int[] GetCategories()
        {
            return Categories;
        }

        public string GetDescription()
        {
            return Description;
        }
        public string GetDate()
        {
            return Date;
        }
        public void AddCategory(int _Category)
        {
            if (Categories[_Category] == 0)
            {
                Categories[_Category] = 1;  
            }
        }

        public void RemoveCategory(int _Category)
        {
            if (Categories[_Category] == 1)
            {
                Categories[_Category] = 0;
            }
        }
    }
}
