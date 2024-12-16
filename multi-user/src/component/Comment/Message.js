import React from 'react';
import { Card } from 'flowbite-react';

const Message = ({ username, comment }) => {
  const isAI = username === "AI";
  return (
    <Card >
      <div className="flex items-center space-x-4">
        <div className="flex items-center justify-center w-10 h-10 rounded-full bg-blue-500 text-white">
          {username}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-gray-500 break-words dark:text-gray-400">
            {comment}
          </p>
        </div>
      </div>
    </Card>
  );
};

export default Message;