import React, { useState } from 'react';
import './App.css';

const App = () => {
  return (
    <div className="app">
      <Header />
      <GameGallery />
      <FeaturedGame />
      <Footer />
    </div>
  );
};

const Header = () => {
  return (
    <header className="header">
      <h1>GameZone</h1>
      <nav>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#games">Games</a></li>
          <li><a href="#about">About</a></li>
        </ul>
      </nav>
    </header>
  );
};

const GameGallery = () => {
  const [games, setGames] = useState([
    { id: 1, name: 'Mini Battles', image: '/Images/Mini Battles.jpeg', url: 'https://poki.com/en/g/12-minibattles', rating: 4.5, comments: ['Amazing gameplay!', 'Loved the storyline.'] },
    { id: 2, name: 'StickMan Crazy', image: '/Images/StickMan Crazy.jpeg', url: 'https://poki.com/en/g/stickman-crazy-box',rating: 4.8, comments: ['Intense action!', 'Best multiplayer experience.'] },
    { id: 3, name: 'Tribals Survival', image: '/Images/Tribals Survival.jpeg', url: 'https://poki.com/en/g/tribals-io',rating: 4.2, comments: ['Beautiful graphics!', 'Engaging quests.'] },
  ]);

  const [selectedGame, setSelectedGame] = useState(null);
  const [newComment, setNewComment] = useState('');

  const handleSelectGame = (game) => {
    setSelectedGame(game);
    setNewComment('');
  };

  const handleAddComment = () => {
    if (newComment.trim() && selectedGame) {
      const updatedGames = games.map((game) => {
        if (game.id === selectedGame.id) {
          return { ...game, comments: [...game.comments, newComment] };
        }
        return game;
      });
      setGames(updatedGames);
      setSelectedGame({ ...selectedGame, comments: [...selectedGame.comments, newComment] });
      setNewComment('');
    }
  };

  return (
    <section className="game-gallery" id="games">
      <h2>Game Gallery</h2>
      <div className="gallery">
        {games.map((game) => (
          <div key={game.id} className="game-card" onClick={() => handleSelectGame(game)}>
            <img src={game.image} alt={game.name} />
            <h3>{game.name}</h3>
            <p>Rating: {game.rating} / 5</p>
            <a href={game.url} target="_blank" rel="noopener noreferrer" className="play-button">Play Now</a>
          </div>
        ))}
      </div>
      {selectedGame && (
        <div className="game-details">
          <h3>Selected Game: {selectedGame.name}</h3>
          <img src={selectedGame.image} alt={selectedGame.name} />
          <p>Experience the thrill of {selectedGame.name}!</p>
          <p>Rating: {selectedGame.rating} / 5</p>
          <h4>Comments:</h4>
          <ul>
            {selectedGame.comments.map((comment, index) => (
              <li key={index}>{comment}</li>
            ))}
          </ul>
          <div className="comment-form">
            <textarea
              placeholder="Add a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
            ></textarea>
            <button onClick={handleAddComment}>Submit</button>
          </div>
        </div>
      )}
    </section>
  );
};

const FeaturedGame = () => {
  const [isPlaying, setIsPlaying] = useState(false);

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };


  return (
    <section className="featured-game">
      <h2>Featured Game</h2>
      <div className="featured-content">
        <img src="/Images/Epic Adventure.jpeg" alt="Featured Game" />
        <div className="info">
          <h3>Epic Adventure</h3>
          <p>Embark on an epic journey through uncharted lands. Discover secrets, battle foes, and become the ultimate hero!</p>
          <button onClick={togglePlay}>{isPlaying ? 'Pause' : 'Play'} Now</button>
        </div>
      </div>
    </section>
  );
};

const Footer = () => {
  return (
    <footer className="footer">
      <p>&copy; 2025 GameZone. All rights reserved.</p>
      <p>Follow us on <a href="#">Twitter</a>, <a href="#">Facebook</a>, and <a href="#">Instagram</a>.</p>
    </footer>
  );
};

export default App;
