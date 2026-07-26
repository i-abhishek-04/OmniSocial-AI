import Navbar from '../components/Navbar/Navbar';
import Hero from '../components/Hero/Hero';
import PlatformGrid from '../components/PlatformGrid/PlatformGrid';
import Features from '../components/Features/Features';
import CTA from '../components/CTA/CTA';
import Footer from '../components/Footer/Footer';

const LandingPage = () => {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <PlatformGrid />
        <Features />
        <CTA />
      </main>
      <Footer />
    </>
  );
};

export default LandingPage;
