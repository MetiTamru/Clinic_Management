// MainComponent.js
import React, { useState, useEffect } from 'react';
import Sidebar from './Sidebar'; 

const MainComponent = () => {
  const [sidebarOpen, setSidebarOpen] = useState(window.innerWidth > 1024);

  const toggleSidebar = (state) => setSidebarOpen(state);

  useEffect(() => {
    const handleResize = () => {
      setSidebarOpen(window.innerWidth > 1024);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className="app-container h-screen">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      <div
        className={`content-container ${sidebarOpen ? "open" : " "}`}
        onClick={() => sidebarOpen && window.innerWidth < 900 && toggleSidebar(false)}
      >
        
      </div>
    </div>
  );
};

export default MainComponent;
