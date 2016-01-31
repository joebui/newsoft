using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace newsoft.Controllers
{
    public class HomeController : Controller
    {
        private readonly NewsEntities _db = new NewsEntities();

        public ActionResult Index()
        {
            // Display all categories on navbar.
            ViewBag.AllCategories = _db.Categories.ToList();
            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
    }
}