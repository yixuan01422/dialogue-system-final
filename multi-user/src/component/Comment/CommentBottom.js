import React, { useEffect, useState } from 'react';
import { Button, Textarea, Select } from 'flowbite-react';
import getReply from '../../util/getReply';

const CommentBottom = ({ addComment }) => {
  const [comment, setComment] = useState('');
  const [reply, setReply] = useState('');
  const [user, setUser] = useState('A');

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (comment === '') {
      alert("Can't send empty message");
      return;
    }
    addComment([
      { user, comment }
    ]);
    setComment('');
    const rep = await getReply(user, comment);
    console.log('Submitted comment:', rep);
    if (rep){
      setReply(rep);
    }
    
  };

  useEffect(() => {
    if (reply !== "") {
      addComment([
        { user: "G", comment: reply }
      ]);
    }
  }, [reply]);

  return (
    <div className="comment-bottom p-4">
      <form onSubmit={handleSubmit} className="comment-form flex flex-col space-y-2">
        <div className="flex space-x-2">
          <Select
            value={user}
            onChange={(e) => setUser(e.target.value)}
            className='user-select w-20'
          >
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
          </Select>
          <Textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Send message"
            className='comment-input flex-grow'
          />
        </div>
        <Button type="submit" color="dark">
          Send
        </Button>
      </form>
    </div>
  );
};

export default CommentBottom;