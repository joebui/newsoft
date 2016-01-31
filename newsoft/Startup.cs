using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(newsoft.Startup))]
namespace newsoft
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
