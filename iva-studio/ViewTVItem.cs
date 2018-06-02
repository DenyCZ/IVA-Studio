using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Media;

namespace ITIM.IVAStudio.Manager
{
    class ViewTVItem : TreeViewItem
    {
        public ImageSource Image { get; private set; }
        public ViewTVItem(ImageSource img) : base()
        {
            this.Image = img;
        }
    }
}
