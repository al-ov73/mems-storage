import React, { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { setMemes } from "../slices/memesSlice";
import { getMemes, getMemesCount } from "../utils/requests.js";
import NavbarPage from "./Navbar.jsx";
import MemesList from "./lists/MemesList.jsx";
import Pagination from 'react-bootstrap/Pagination';
import WelcomeModal from "./modals/WelcomeModal.jsx";

const paginationRangeLimit = 2;

const createRange = (number) => {
  const result = [];
  for (let i = number - paginationRangeLimit; i <= number + paginationRangeLimit; i++) {
    result.push(i);
  }
  return result;
}


const IndexPage = () => {
  const dispatch = useDispatch();
  const [memeOffset, setMemeOffset] = useState(0);
  const [welcomeModalShow, setWelcomeModalShow] = useState(true);
  const [memesCount, setMemesCount] = useState(0);

  const memesPerPage = Number(process.env.REACT_APP_MEMES_PER_PAGE);
  const activePage = (memeOffset / memesPerPage) + 1;
  const maxPages = Math.ceil(memesCount / memesPerPage)

  // get memes
  useEffect(() => {
    const inner = async () => {
      try {
        const response = await getMemes(access_token, memeOffset, memesPerPage);
        dispatch(setMemes(response.data));
        const countResponse = await getMemesCount(access_token);
        setMemesCount(countResponse.data.total)
      } catch (e) {
        console.log('memes get error');
        console.log(e)
        dispatch(setMemes([]))
      }
    }
    inner();
  }, [memeOffset]);

  const access_token = localStorage.getItem('user')

  const handleChangePage = (e) => {
    const newActivePage = Number(e.target.text);
    const newOffset = (newActivePage - 1) * memesPerPage;
    setMemeOffset(newOffset);
  }

  const generatePagiantion = () => {
    let items = [];
    const paginationRange = createRange(activePage);

    if ((activePage - paginationRangeLimit) > 1) {
      items.push(<Pagination.Ellipsis key={0} disabled />)
    }

    for (let number = 1; number <= maxPages; number++) {
      if (paginationRange.includes(number)) {
        items.push(
          <Pagination.Item key={number} active={number === activePage} onClick={handleChangePage}>
            {number}
          </Pagination.Item>,
        );
      }
    }
    if ((maxPages - activePage) > paginationRangeLimit) {
      items.push(<Pagination.Ellipsis key={maxPages + 1} disabled />)
    }

    return items;
  }

  const paginationItems = generatePagiantion();

  const handleNext = () => {
    if (activePage < maxPages) {
      setMemeOffset(memeOffset + memesPerPage);
    }
  }

  const handlePrev = () => {
    if (activePage > 1) {
      setMemeOffset(memeOffset - memesPerPage);
    }
  }

  const handleLast = () => {
    const newOffset = (maxPages - 1) * memesPerPage;
    setMemeOffset(newOffset);
  }

  return (
    <>
      <WelcomeModal
        show={welcomeModalShow}
        onHide={() => setWelcomeModalShow(false)}
      />

      <NavbarPage full={true} />

      {/* PAGINATION */}
      <Container>
        <Pagination className="my-2 justify-content-center">
          <Pagination.First onClick={() => setMemeOffset(0)} />
          <Pagination.Prev onClick={handlePrev} />
          {paginationItems}
          <Pagination.Next onClick={handleNext} />
          <Pagination.Last onClick={handleLast} />
        </Pagination>
      </Container>
      {/* END PAGINATION */}

      <Container className="d-flex">
        <Container>
          <Row>
            <MemesList />
          </Row>
        </Container>
      </Container>

      {/* PAGINATION */}
      <Container>
        <Pagination className="my-2 justify-content-center">
          <Pagination.First onClick={() => setMemeOffset(0)} />
          <Pagination.Prev onClick={handlePrev} />
          {paginationItems}
          <Pagination.Next onClick={handleNext} />
          <Pagination.Last onClick={handleLast} />
        </Pagination>
      </Container>
      {/* END PAGINATION */}

    </>
  );
}

export default IndexPage;