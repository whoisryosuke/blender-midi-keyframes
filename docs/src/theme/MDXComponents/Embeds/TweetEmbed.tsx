import React from "react";

type Props = {
  username: string;
  id: string;
};
const TweetEmbed = ({ id, username = "whoisryosuke" }: Props) => {
  return (
    <div style={{ width: "100%", marginBottom: "16px" }}>
      <script src="https://platform.twitter.com/widgets.js" />
      <blockquote className="twitter-tweet">
        <p>Loading tweet...</p>
        <a
          href={`https://twitter.com/${username}/status/${id}?ref_src=twsrc%5Etfw`}
        >
          Loading date...
        </a>
      </blockquote>
    </div>
  );
};

export default TweetEmbed;
