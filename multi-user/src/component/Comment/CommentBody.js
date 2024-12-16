import React, { useEffect, useRef } from 'react';
import { Card } from 'flowbite-react';
import Message from './Message';

const CommentBody = ({ comments }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [comments]);

  return (
    <div className="comment-body overflow-y-auto max-h-96 h-96">
      {comments.length > 0 ? (
        comments.map((comment, index) => (
          <Card key={index} className="mb-2">
            <Message
              icon={comment.user === 'AI' ? 'logo192.png' : 'user.png'}
              username={comment.user}
              comment={comment.comment}
            />
          </Card>
        ))
      ) : (
        <div className="flex items-center justify-center h-full">
          <p className="text-gray-500">No message yet</p>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
};

export default CommentBody;