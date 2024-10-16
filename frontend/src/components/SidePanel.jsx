import React, { useState, useEffect } from "react";
import SpinnerEl from './spinners/SimpleSpinner';
import { getTopLikedMemes } from "../utils/requests";


const SidePanel = () => {
  const [isLoading, setLoading] = useState(true);
  const [topLikedMemes, setTopLikedMemes] = useState([])

  const access_token = localStorage.getItem('user')

  // get top liked memes
  useEffect(() => {
    const inner = async () => {
      const response = await getTopLikedMemes(access_token);
      setTopLikedMemes(response);
      setLoading(false);
    }
    inner();
  }, [])

  console.log('topLikedMemes', topLikedMemes)

  if (isLoading) {
    return <SpinnerEl/>
  }

  return (
    <>
      <div className="sidebar" role="cdb-sidebar">
        <div className="sidebar-container">
          <div className="sidebar-nav">
            <div className="sidenav">

              <a className="sidebar-item">
                <div className="sidebar-item-content">
                  <i className="fa fa-th-large sidebar-icon sidebar-icon-lg"></>
                  <span>Dashboard</span>
                  <div className="suffix">
                    <div className="badge rounded-pill bg-danger">new</div>
                  </div>
                </div>
              </a>

            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default SidePanel;