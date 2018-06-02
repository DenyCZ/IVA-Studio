using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ITIM.IVAStudio.Manager
{
    abstract public class ProtobufTranscoder
    {
        // TODO
    }

    abstract public class SharedStorage
    {
        //public byte[] Get(String key);
        
        public void Set(String key, byte[] data)
        {
            throw new NotImplementedException();
        }
        public String UniqueKey()
        {
            throw new NotImplementedException();
        }
    }
}
