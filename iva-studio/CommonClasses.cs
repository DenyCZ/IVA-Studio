using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ITIM.IVAStudio.Manager
{
    public class AnnotatedCamera
    {
        // TODO
    }
    public class AnnotatedCameraRoutingKey
    {
        public AnnotatedCamera camera;
        public List<String> routing_key;
        public AnnotatedCameraRoutingKey(AnnotatedCamera camera, String routing_key)
        {
            this.camera = camera;
            this.routing_key = new List<String>(routing_key.Split('.'));
        }
        
        

    }
}