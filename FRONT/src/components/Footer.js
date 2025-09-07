import React from "react";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h2>Contact</h2>
          <p>
            Email :{" "}
            <a href="mailto:contact@projetAIS.com">contact@projetAIS.com</a>
          </p>
          <p>
            Téléphone : <a href="tel:+33123456789">+33 1 23 45 67 89</a>
          </p>
        </div>

        <div className="footer-section">
          <h4>Suivez-nous</h4>
          <div className="social-icons">
            <a
              href="https://facebook.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              Facebook
            </a>
            <br />
            <a
              href="https://twitter.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              Twitter
            </a>
            <br />
            <a
              href="https://linkedin.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              LinkedIn
            </a>
          </div>
        </div>

        <div className="footer-section">
          <h4>Informations</h4>
          <p>
            <a href="/mentions-legales">Mentions légales</a>
          </p>
          <p>
            <a href="/politique-confidentialite">
              Politique de confidentialité
            </a>
          </p>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} MonSite - Tous droits réservés</p>
      </div>
    </footer>
  );
}
export default Footer;
