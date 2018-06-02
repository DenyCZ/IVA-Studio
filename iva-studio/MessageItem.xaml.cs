using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ITIM.IVAStudio.Manager
{

    /// <summary>
    /// Interakční logika pro MessageItem.xaml
    /// </summary>
    public partial class MessageItem : TreeViewItem
    {
        private AnnotatedCameraRoutingKey msg;



        public MessageItem(AnnotatedCameraRoutingKey msg)
        {
            this.msg = msg;
            InitializeComponent();
            this.MsgHeader.Header = String.Format("[{0}] {1}", DateTime.Now.ToString("HH:mm:ss.fff"), String.Join(".", msg.routing_key.ToArray()));

            for(int i = 1; i < 6; i++) this.Camera.Items.Add(new ViewTVItem(new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "imageph.png", UriKind.Absolute))) { Header = "View#" + i });
        }
    }
}
