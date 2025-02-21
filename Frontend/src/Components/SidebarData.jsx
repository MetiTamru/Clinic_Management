import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTachometerAlt,faTruck,  faChartBar, faCogs, faChartLine, faCreditCard,  faListAlt, faBoxes, faReceipt, faCashRegister, faBoxOpen, faCubes, faFileInvoice, faUserTie, faCalendarAlt, faUndo, faChartPie, faAreaChart, faUsersCog, faBell, faExclamationTriangle, faEnvelopeOpenText, faUserFriends, faGift, faCog, faExchangeAlt, faUserPlus, faSearch, faMoneyBill1Wave, faFileInvoiceDollar, faFolderPlus, faFolder, faShoppingCart, faExchange, faUser, faDollyFlatbed, faList12, faList ,faClipboardList, faUsersGear, faUserCog} from "@fortawesome/free-solid-svg-icons";

import { faMicrosoft } from "@fortawesome/free-brands-svg-icons";
import { faUserInjured } from "@fortawesome/free-solid-svg-icons";


export const SidebarData = [
  {
    title: 'Dashboard',
    path: '/',
    icon:<FontAwesomeIcon icon={faMicrosoft} />,
    roles: ["admin",""],
  },
  
  {
    title: 'Manage Patient',
    path: '/manage-patient',
    icon: <FontAwesomeIcon icon={faUserInjured} />,
    roles: ["admin", ""],

    
    subNav: [
      {
        title: 'Add Patient',
        path: '/manage-patient/add-patient',
        icon: <FontAwesomeIcon icon={faUserPlus} />,
        roles: ["admin", ""],

      },
      {
        title: 'Patient List',
        path: '/manage-patient/patient-list',
        icon: <FontAwesomeIcon icon={faClipboardList} />,
        roles: ["admin", ""],

      },
    ]
  },
 
  {
    title: 'Manage Employees',
    path: '/manage-employees',
    icon: <FontAwesomeIcon icon={faUsersGear} />,
    roles: [""],
    subNav: [
      {
        title: 'Add Employee',
        path: '/manage-employees/add-employees',
        icon: <FontAwesomeIcon icon={faUserPlus} />,
        roles: ["admin", ""],

      },
      {
        title: 'Employee List',
        path: '/manage-employees/employee-list',
        icon: <FontAwesomeIcon icon={faClipboardList} />,
        roles: ["admin", ""],

      },]

  },
  {
        title: 'Manage Roles',
        path: '/manage-roles',
        icon: <FontAwesomeIcon icon={faUserCog} />,
        roles: ["admin",""],
        subNav: [
          {
            title: 'Add Role',
            path: '/manage-roles/add-role',
            icon: <FontAwesomeIcon icon={faUserPlus} />,
            roles: ["admin", ""],
    
          },
          {
            title: ' Role List',
            path: '/manage-roles/role-list',
            icon: <FontAwesomeIcon icon={faClipboardList} />,
            roles: ["admin", "ghh"],
    
          },]
  },
//   {
//     title: 'Expenses',
//     path: '/expenses',
//     icon: <FontAwesomeIcon icon={faMoneyBill1Wave} />,
//     roles: ["cash"],
//     subNav: [
      
//       {
//         title: 'Add Expenses',
//         path: '/expenses/add',
//         icon: <FontAwesomeIcon icon={faFileInvoiceDollar} />,
//         roles: [""],
//       },
//       {
//         title: ' Expense Report',
//         path: '/expenses/report',
//         icon: <FontAwesomeIcon icon={faListAlt} />,
//         roles: [""],
//       },
      
//     ],
//   },
//   {
//     title: ' Expense Report',
//     path: '/expenses/report',
//     icon: <FontAwesomeIcon icon={faListAlt} />,
//     roles: [""],
//   },
//   {
//     title: 'Sell',
//     path: '/sell',
//     icon: <FontAwesomeIcon icon={faShoppingCart} />,
//     roles: ["admin",""],
//     subNav: [
//       {
//         title: 'View Sales ',
//         path: '/sell/view-sell',
//         icon: <FontAwesomeIcon icon={faChartLine} />,
//         roles: ["admin"],
//       },]
//   },
//   {
//     title: 'Debit Report',
//         path: '/debit-report',
//         icon: <FontAwesomeIcon icon={faReceipt} />,
//         roles: [""],
    
//   },
//   {
//     title: 'Exchange Report',
//         path: '/exchange/report',
//         icon: <FontAwesomeIcon icon={faExchange} />,
//         roles: [""],
    
//   },
//   {
//         title: 'Submit to Bank',
//         path: '/submit-revenue',
//         icon: <FontAwesomeIcon icon={faDollyFlatbed} />,
//         roles: ["admin",''],
       
//   },
// {
//            title: 'Bank Transfer Report',
//             path: '/revenue-report',
//             icon: <FontAwesomeIcon icon={faReceipt }  />, 
//             roles: [""],
//             subNav: [
//               {
//                 title: 'History',
//                 path: '/revenue-report/history',
//                 icon: <FontAwesomeIcon icon={faList} />,
//                 roles: [""],
//               },]
// },
// {
//   title: 'Bank Transfer Report',
//    path: '/revenue-report/history',
//    icon: <FontAwesomeIcon icon={faReceipt }  />, 
//    roles: [""],
  
// },
 
//   {
//     title: 'Cashier Management',
//     path: '/cashier-management',
//     icon: <FontAwesomeIcon icon={faUserFriends} />,
//     roles: ["admin"],
//     subNav: [
      
//       {
//         title: 'Register Cashier',
//         path: '/cashier-management/register',
//         icon: <FontAwesomeIcon icon={faUserPlus} />, 
//         roles: ["admin"],
//       },
      
      
//     ],
//   },
];
