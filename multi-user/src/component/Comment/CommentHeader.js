import React from 'react';
import { Navbar } from 'flowbite-react';

const CommentHeader = () => {
  return (
    <Navbar fluid={true} rounded={true}>
      <Navbar.Brand href="#">
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
          Chat
        </span>
      </Navbar.Brand>
    </Navbar>
  );
};

export default CommentHeader;