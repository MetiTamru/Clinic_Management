import React, { useState, useEffect,useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faTimes, faChevronDown, faChevronRight } from "@fortawesome/free-solid-svg-icons";
import { SidebarData } from "./SidebarData";
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { faSignOutAlt } from "@fortawesome/free-solid-svg-icons";

const Sidebar = ({ isOpen, setIsOpen }) => {
  const [expandedMenus, setExpandedMenus] = useState({});
  const [isHovered, setIsHovered] = useState(false);
  const location = useLocation();
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const sidebarRef = useRef(null); // Ref for sidebar


  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        sidebarRef.current && 
        !sidebarRef.current.contains(event.target) && 
        window.innerWidth <= 768
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [setIsOpen]);

  const toggleSubMenu = (index) => {
    setExpandedMenus((prev) => ({
      [index]: !prev[index],
    }));
  };

  const itemVariants = {
    hidden: { opacity: 0, y: -10 },
    visible: { opacity: 1, y: 0 },
  };

  const containerVariants = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: 0.1,
      },
    },
    exit: {
      transition: {
        staggerChildren: 0.12,
        delayChildren: 0.1,
      },
    },
  };

  const isActiveLink = (path) => location.pathname === path;
  const isSmallScreen = windowWidth <= 640; // Check if screen is small

  const handleLogout = () => {
    // Clear authentication (Example: Remove token)
    localStorage.removeItem("token"); 
    // Redirect to login page
    window.location.href = "/login"; 
  };

  return (
<motion.div
  ref={sidebarRef}
  className="fixed top-14 left-0 h-full bg-white text-gray-800 transition-all ease-in-out border-r border-gray-200 flex flex-col justify-between"
  animate={{ width: isOpen || (!isSmallScreen && isHovered) ? 260 : isSmallScreen ? 0 : 62 }}
  transition={{ duration: 0.2, ease: "easeOut" }}
  onMouseEnter={() => !isSmallScreen && setIsHovered(true)}
  onMouseLeave={() => !isSmallScreen && setIsHovered(false)}
>
  {/* Sidebar Items */}
  <ul className="mt-4 overflow-y-auto scrollbar-hide flex-grow">
    {SidebarData.map((item, index) => (
      <li key={index} className="relative">
        <div
          className={`rounded-md ml-4 mt-3 mb-2 mr-4 hover:bg-gray-100 flex items-center justify-between cursor-pointer ${
            isActiveLink(item.path) ? "bg-[#CEEFFE] text-[#04577e]" : ""
          }`}
          onClick={() => item.subNav && toggleSubMenu(index)}
        >
          <Link to={item.path} className="flex items-center gap-3 w-full">
            {(isOpen || !isSmallScreen) && (
              <>
                <div className="pl-2 w-6 flex justify-center">{item.icon}</div>
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: isHovered || isOpen ? 1 : 0 }}
                  transition={{ duration: 0.2 }}
                  className="h-14 pt-4 pl-4"
                >
                  {item.title}
                </motion.span>
              </>
            )}
          </Link>
          {item.subNav && (
            <FontAwesomeIcon
              icon={expandedMenus[index] ? faChevronDown : faChevronRight}
              className={`ml-auto transition-all duration-50 ease-in-out ${
                isHovered || isOpen ? "block" : "invisible"
              }`}
            />
          )}
        </div>
        {item.subNav && expandedMenus[index] && (isHovered || isOpen) && (
          <motion.ul
            className="pl-8 ml-7 mr-7 mt-4 py-2 bg-gray-50"
            initial="hidden"
            animate="visible"
            exit="exit"
            variants={containerVariants}
          >
            {item.subNav.map((subItem, subIndex) => (
              <motion.li
                key={subIndex}
                className={`p-4 hover:bg-gray-100  ${
                  isActiveLink(subItem.path) ? "bg-[#CEEFFE]" : ""
                }`}
                variants={itemVariants}
              >
                <Link to={subItem.path} className="flex items-center gap-3">
                  {subItem.icon} <span>{subItem.title}</span>
                </Link>
              </motion.li>
            ))}
          </motion.ul>
        )}
      </li>
    ))}
  </ul>

  {/* ✅ Logout Button Fixed at Bottom */}
  <div className="p-4 mb-12 border-t border-gray-300">
    <button
      className="w-full flex items-center justify-start px-4 py-3 text-red-600 hover:bg-red-100 rounded-md transition-all"
      onClick={handleLogout}
    >
      <FontAwesomeIcon icon={faSignOutAlt} className="mr-3" />
      {isOpen || isHovered ? "Logout" : ""}
    </button>
  </div>
</motion.div>

  );
};

const Navbar = ({ isSidebarOpen, setIsSidebarOpen }) => {
  const handleToggleClick = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <nav className="bg-white border-b border-gray-200 text-gray-800 p-4 fixed justify-between flex w-full items-center">
      {/* Flex container to align label & button */}
      <div className="flex items-center gap-32">
      <h1 className="text-lg ml-1 font-bold text-[#0B597F]">AHM <span className="text-gray-800">-Tech</span></h1>

        <button onClick={handleToggleClick} className="text-gray-800 focus:outline-none">
          <FontAwesomeIcon icon={isSidebarOpen ? faTimes : faBars} />
        </button>
      </div>
<div className="flex justify lg:mr-10">
  <div> <img src="" alt="" />
  </div> 
  <div><p className="text-gray-800 font-bold text-lg">Full Name</p><p className="text-xs">Name@gmail.com</p></div>
</div>
    </nav>
  );
};

const Layout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setIsSidebarOpen(true);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div>
      <Navbar isSidebarOpen={isSidebarOpen} setIsSidebarOpen={setIsSidebarOpen} />
      <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />
    </div>
  );
};

export default Layout;
