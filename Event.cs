using System;
using System.Collections.Generic;
using System.Text;

namespace ResponseParser
{

    class Event
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

        int GetID()
        {
            return ID;
        }

        string GetName()
        {
            return Name;
        }

        string GetLocation()
        {
            return Location;
        }

        int[] GetCategories()
        {
            return Categories;
        }

        string GetDescription()
        {
            return Description;
        }
        string GetDate()
        {
            return Date;
        }
        void AddCategory(int _Category)
        {
            if (Categories[_Category] == 0)
            {
                Categories[_Category] = 1;  
            }
        }

        void RemoveCategory(int _Category)
        {
            if (Categories[_Category] == 1)
            {
                Categories[_Category] = 0;
            }
        }
    }
}
