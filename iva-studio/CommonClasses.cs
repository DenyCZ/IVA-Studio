using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace iva_studio
{
    class AnnotatedCamera
    {
        // TODO
    }
    class AnnotatedCameraRoutingKey
    {
        AnnotatedCamera camera;
        List<String> routing_key;
        public AnnotatedCameraRoutingKey(AnnotatedCamera camera, String routing_key)
        {
            this.camera = camera;
            this.routing_key = List<String>();
        }
        
        

    }
}