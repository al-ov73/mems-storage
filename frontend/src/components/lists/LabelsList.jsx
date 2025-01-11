import React from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import LabelPostForm from "../forms/LabelPostForm";


const LabelsList = ({ currentMeme, username, memeOffset, memesPerPage }) => {
    const handleLabelDelete = () => {}

    return <Row xs="auto" className="my-3">
        {currentMeme.meme_labels && currentMeme.meme_labels.map((label) => {
            return <Col key={label.id} className="my-1">
                <Button className="rounded-pill"
                    disabled={!Boolean(username)}
                    variant="warning"
                    size="sm"
                    onClick={handleLabelDelete}>
                    {label.title}
                </Button>
            </Col>
        })}

        {/* LABEL POST FORM */}
        {username && <LabelPostForm meme={currentMeme} memeOffset={memeOffset} memesPerPage={memesPerPage} />}
        {/* END LABEL POST FORM */}

    </Row>
}

export default LabelsList;