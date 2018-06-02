using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ITIM.IVAStudio
{
    public delegate void AddedItemHandler(object sender, AddedItemEventArgs e);

    public class ControlledList<T> : List<T>
    {
        public event AddedItemHandler OnAddedItem;

        public void Add(T item)
        {
            if (OnAddedItem != null) OnAddedItem(this, new AddedItemEventArgs(item, typeof(T)));
            base.Add(item);
        }
    }

    public class AddedItemEventArgs : EventArgs
    {
        public object Item { get; private set; }
        public Type Type { get; private set; }

        public AddedItemEventArgs(object item, Type type)
        {
            this.Item = item;
            this.Type = type;
        }
    }
}
