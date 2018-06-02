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
using System.ComponentModel;
using ITIM.IVAStudio;

namespace ITIM.IVAStudio.Manager
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        ControlledList<AnnotatedCameraRoutingKey> CameraRoutingKeys;

        BackgroundWorker recordingsimulator = new BackgroundWorker();

        public MainWindow()
        {
            CameraRoutingKeys = new ControlledList<AnnotatedCameraRoutingKey>();
            InitializeComponent();
            recordingsimulator.DoWork += new DoWorkEventHandler(SimulateRecording);
            recordingsimulator.WorkerSupportsCancellation = true;
        }

        private void ViewChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
        {
            ImageSource img = (e.NewValue as ViewTVItem)?.Image;
            ViewImg.Source = img;
        }

        private void ClearList(object sender, RoutedEventArgs e)
        {
            this.MsgTV.Items.Clear();
        }
        

        //DEBUG

        List<string> debug_rks = new List<string>() { "pes", "kocka", "zirafa", "delfin", "krava", "hroch", "slon", "aligator", "lev", "tygr", "leopard", "kosatka", "plejtvak", "pstros", "korela", "ara" };

        private void StartStopRecording(object sender, RoutedEventArgs e)
        {
            if (recordingsimulator.IsBusy)
            {
                recordingsimulator.CancelAsync();
                StartButton.Content = "START";
                MenuStart.IsEnabled = true;
                MenuStop.IsEnabled = false;
            }
            else
            {
                recordingsimulator.RunWorkerAsync();
                StartButton.Content = "STOP";
                MenuStart.IsEnabled = false;
                MenuStop.IsEnabled = true;
            }
        }

        private void SimulateRecording(object sender, DoWorkEventArgs e)
        {
            while (true)
            {
                Random rnd = new Random();
                BackgroundWorker bw = sender as BackgroundWorker;
                Application.Current.Dispatcher.BeginInvoke(
                    System.Windows.Threading.DispatcherPriority.Background,
                    new Action(() => this.CameraRoutingKeys.Add(new AnnotatedCameraRoutingKey(new AnnotatedCamera(), String.Format("{0}.{1}.{2}.{3}", debug_rks[rnd.Next(0, debug_rks.Count)], debug_rks[rnd.Next(0, debug_rks.Count)], debug_rks[rnd.Next(0, debug_rks.Count)], debug_rks[rnd.Next(0, debug_rks.Count)]))))
                );
                System.Threading.Thread.Sleep(rnd.Next(0, 1001));
                if(bw.CancellationPending)
                {
                    e.Cancel = true;
                    return;
                }
            }
        }
    }
}
