import React, { useState } from 'react';
import CommentHeader from './CommentHeader';
import CommentBottom from './CommentBottom';
import CommentBody from './CommentBody';

function Comment({  }) {
  const [comments, setComments] = useState([]);

  const addComment = (newComments) => {
    setComments([...comments, ...newComments]);
  };

  return (
    <div className="comment-container max-w-md mx-auto bg-white shadow-md rounded-lg overflow-hidden">
      <CommentHeader />
      <CommentBody comments={comments} />
      <CommentBottom addComment={addComment} />
    </div>
  );
}

export default Comment;