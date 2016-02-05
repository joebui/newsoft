using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.UI.WebControls;

namespace newsoft.Controllers
{
    public class HomeController : Controller
    {
        private readonly NewsEntities _db = new NewsEntities();

        public ActionResult Index()
        {
            // Display all categories on navbar.
            ViewBag.AllCategories = _db.Categories.ToList();
            // DIsplay 3 most viewed news.
            ViewBag.TopViewed = _db.News.OrderByDescending(n => n.viewed).Take(3).ToList();
            // Display 4 latest news
            var allNews = _db.News.OrderByDescending(n => n.id).ToList();
            return View(allNews);
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