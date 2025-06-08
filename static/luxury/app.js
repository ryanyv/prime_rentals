// Application Data
const appData = {
  shortTermProperties: [
    {
      id: 1,
      title: "Luxury Downtown Penthouse",
      price: 350,
      location: "Downtown Core, Financial District",
      guests: 6,
      bedrooms: 3,
      bathrooms: 2,
      amenities: ["WiFi", "Kitchen", "Parking", "Pool", "Gym", "Balcony", "Concierge"],
      available: ["2025-06-08", "2025-06-09", "2025-06-10", "2025-06-15", "2025-06-16"],
      image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400&h=300&fit=crop",
      rating: 4.9,
      type: "Entire place",
      features: ["City View", "Luxury Amenities", "Prime Location"]
    },
    {
      id: 2,
      title: "Modern Waterfront Villa",
      price: 280,
      location: "Marina Bay, Waterfront",
      guests: 8,
      bedrooms: 4,
      bathrooms: 3,
      amenities: ["WiFi", "Kitchen", "Parking", "Pool", "Gym", "Beach Access", "Spa"],
      available: ["2025-06-12", "2025-06-13", "2025-06-14", "2025-06-20", "2025-06-21"],
      image: "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop",
      rating: 4.8,
      type: "Entire place",
      features: ["Ocean View", "Private Beach", "Luxury Villa"]
    },
    {
      id: 3,
      title: "Boutique City Loft",
      price: 180,
      location: "Arts District, Creative Quarter",
      guests: 4,
      bedrooms: 2,
      bathrooms: 1,
      amenities: ["WiFi", "Kitchen", "Parking", "Balcony", "Art Gallery"],
      available: ["2025-06-10", "2025-06-11", "2025-06-12", "2025-06-18", "2025-06-19"],
      image: "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400&h=300&fit=crop",
      rating: 4.7,
      type: "Entire place",
      features: ["Modern Design", "Arts District", "Creative Space"]
    }
  ],
  longTermProperties: [
    {
      id: 4,
      title: "Executive Luxury Apartment",
      rent: 4500,
      location: "Business District, Central",
      bedrooms: 3,
      bathrooms: 2,
      sqft: 1800,
      amenities: ["Parking", "Gym", "Concierge", "Pool", "Garden", "Business Center"],
      lease: "12 months minimum",
      furnished: true,
      pets: true,
      image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400&h=300&fit=crop",
      available: "Immediate",
      features: ["Executive Building", "Business District", "Luxury Amenities"]
    },
    {
      id: 5,
      title: "Modern Family Townhouse",
      rent: 3200,
      location: "Residential Hills, Family District",
      bedrooms: 4,
      bathrooms: 3,
      sqft: 2400,
      amenities: ["Parking", "Garden", "Schools Nearby", "Shopping Center", "Playground"],
      lease: "6 months minimum",
      furnished: false,
      pets: true,
      image: "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=400&h=300&fit=crop",
      available: "July 1st",
      features: ["Family Friendly", "Great Schools", "Quiet Neighborhood"]
    },
    {
      id: 6,
      title: "Studio Loft Professional",
      rent: 1800,
      location: "Tech Hub, Innovation District",
      bedrooms: 1,
      bathrooms: 1,
      sqft: 800,
      amenities: ["WiFi", "Gym", "Coworking Space", "Parking", "Rooftop"],
      lease: "6 months minimum",
      furnished: true,
      pets: false,
      image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&h=300&fit=crop",
      available: "June 15th",
      features: ["Tech Hub", "Modern Amenities", "Professional Living"]
    }
  ]
};

// DOM Elements
const searchTabs = document.querySelectorAll('.search-tab');
const searchContainers = document.querySelectorAll('.search-container');
const propertyToggle = document.querySelectorAll('.toggle-btn');
const propertyGrids = document.querySelectorAll('.property-grid');
const filterPills = document.querySelectorAll('.filter-pill');
const searchButtons = document.querySelectorAll('.search-btn');
let guestField, guestMenu, guestsInput, guestsDisplay, adultsCountEl, childrenCountEl;
let adults = 1;
let children = 0;

// Initialize the application
function initLuxuryPage() {
  initializeApp();
  populateLocationOptions();
  setDefaultDates();
  applyQueryParams();
  initDatePicker();
  renderProperties();
  setupEventListeners();
  setupGuestDropdown();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initLuxuryPage);
} else {
  initLuxuryPage();
}

function initializeApp() {
  // Set initial active states
  document.querySelector('[data-tab="short-term"]').classList.add('active');
  document.querySelector('#short-term-search').classList.add('active');
  document.querySelector('[data-type="short-term"]').classList.add('active');
  document.querySelector('#short-term-properties').classList.add('active');
}

function populateLocationOptions() {
  const locations = [...appData.shortTermProperties, ...appData.longTermProperties]
    .map(p => p.location);
  const unique = [...new Set(locations)];
  ['location-short', 'location-long'].forEach(id => {
    const select = document.getElementById(id);
    if (select) {
      select.innerHTML = '<option value="">All Locations</option>' +
        unique.map(loc => `<option value="${loc}">${loc}</option>`).join('');
    }
  });
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function formatDateTime(date) {
  return (
    date.getFullYear() +
    '-' +
    String(date.getMonth() + 1).padStart(2, '0') +
    '-' +
    String(date.getDate()).padStart(2, '0') +
    ' ' +
    String(date.getHours()).padStart(2, '0') +
    ':' +
    String(date.getMinutes()).padStart(2, '0')
  );
}

function setDefaultDates() {
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  document.getElementById('checkin').value = formatDateTime(today);
  document.getElementById('checkout').value = formatDateTime(tomorrow);
  document.getElementById('daterange').value =
    formatDateTime(today) + ' to ' + formatDateTime(tomorrow);
  document.getElementById('movein').value = formatDate(today);
}

function initDatePicker() {
  if (typeof flatpickr === 'undefined') return;
  flatpickr('#daterange', {
    mode: 'range',
    enableTime: true,
    dateFormat: 'Y-m-d H:i',
    minDate: 'today',
    defaultDate: [
      document.getElementById('checkin').value,
      document.getElementById('checkout').value
    ],
    onChange: function(selectedDates) {
      if (selectedDates.length === 2) {
        document.getElementById('checkin').value = formatDateTime(selectedDates[0]);
        document.getElementById('checkout').value = formatDateTime(selectedDates[1]);
      }
    }
  });
}

function setupEventListeners() {
  // Search tab switching
  searchTabs.forEach(tab => {
    tab.addEventListener('click', handleSearchTabSwitch);
  });
  
  // Property type toggle
  propertyToggle.forEach(btn => {
    btn.addEventListener('click', handlePropertyToggle);
  });
  
  // Filter pills
  filterPills.forEach(pill => {
    pill.addEventListener('click', handleFilterToggle);
  });
  
  // Search buttons
  searchButtons.forEach(btn => {
    btn.addEventListener('click', handleSearch);
  });
  
  // Smooth scrolling for navigation
  document.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', handleSmoothScroll);
  });
}

function setupGuestDropdown() {
  guestField = document.querySelector('.guest-field');
  if (!guestField) return;
  guestMenu = guestField.querySelector('.guest-menu');
  guestsInput = document.getElementById('guests');
  guestsDisplay = document.getElementById('guests-display');
  adultsCountEl = document.getElementById('adults-count');
  childrenCountEl = document.getElementById('children-count');

  updateGuestDisplay();

  guestsDisplay.addEventListener('click', () => {
    guestField.classList.toggle('active');
  });

  document.addEventListener('click', (e) => {
    if (!guestField.contains(e.target)) {
      guestField.classList.remove('active');
    }
  });

  guestMenu.querySelectorAll('.guest-plus').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      changeGuestCount(btn.dataset.type, 1);
    });
  });
  guestMenu.querySelectorAll('.guest-minus').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      changeGuestCount(btn.dataset.type, -1);
    });
  });
}

function changeGuestCount(type, delta) {
  if (type === 'adults') {
    adults = Math.max(1, adults + delta);
  } else {
    children = Math.max(0, children + delta);
  }
  updateGuestDisplay();
}

function updateGuestDisplay() {
  if (!guestsDisplay) return;
  adultsCountEl.textContent = adults;
  childrenCountEl.textContent = children;
  const total = adults + children;
  guestsInput.value = total;
  guestsDisplay.value = `${adults} adult${adults > 1 ? 's' : ''}${children > 0 ? ", " + children + " child" + (children > 1 ? 'ren' : '') : ''}`;
}

function applyQueryParams() {
  const params = new URLSearchParams(window.location.search);
  if (!params.has('mode')) return;

  const isShort = params.get('mode') === 'short';
  const tab = isShort ? 'short-term' : 'long-term';

  // activate correct tab and grid
  document.querySelectorAll('.search-tab').forEach(t => t.classList.remove('active'));
  const tabBtn = document.querySelector(`[data-tab="${tab}"]`);
  if (tabBtn) tabBtn.classList.add('active');

  searchContainers.forEach(c => c.classList.remove('active'));
  const activeSearch = document.getElementById(`${tab}-search`);
  if (activeSearch) activeSearch.classList.add('active');

  propertyToggle.forEach(b => b.classList.remove('active'));
  const toggleBtn = document.querySelector(`.toggle-btn[data-type="${tab}"]`);
  if (toggleBtn) toggleBtn.classList.add('active');

  propertyGrids.forEach(g => g.classList.remove('active'));
  const activeGrid = document.getElementById(`${tab}-properties`);
  if (activeGrid) activeGrid.classList.add('active');

  if (isShort) {
    if (params.get('location')) document.getElementById('location-short').value = params.get('location');
    if (params.get('checkin')) document.getElementById('checkin').value = params.get('checkin');
    if (params.get('checkout')) document.getElementById('checkout').value = params.get('checkout');
    if (params.get('checkin') && params.get('checkout')) {
      document.getElementById('daterange').value =
        params.get('checkin') + ' to ' + params.get('checkout');
    }
    if (params.get('guests')) {
      document.getElementById('guests').value = params.get('guests');
      adults = parseInt(params.get('adults') || params.get('guests')) || 1;
      children = parseInt(params.get('children') || 0);
      updateGuestDisplay();
    }
  } else {
    if (params.get('location')) document.getElementById('location-long').value = params.get('location');
    if (params.get('movein')) document.getElementById('movein').value = params.get('movein');
    if (params.get('lease')) document.getElementById('lease').value = params.get('lease');
    if (params.get('budget')) document.getElementById('budget').value = params.get('budget');
  }

  const searchParams = getSearchParameters(isShort);
  const filtered = filterProperties(searchParams, isShort);
  renderFilteredProperties(filtered, isShort);
  if (document.getElementById('properties')) {
    document.getElementById('properties').scrollIntoView();
  }

  history.replaceState(null, '', window.location.pathname);
}

function handleSearchTabSwitch(e) {
  const targetTab = e.target.dataset.tab;
  
  // Update tab states
  searchTabs.forEach(tab => tab.classList.remove('active'));
  e.target.classList.add('active');
  
  // Update search container states
  searchContainers.forEach(container => {
    container.classList.remove('active');
  });
  document.getElementById(`${targetTab}-search`).classList.add('active');
}

function handlePropertyToggle(e) {
  const targetType = e.target.dataset.type;
  
  // Update button states
  propertyToggle.forEach(btn => btn.classList.remove('active'));
  e.target.classList.add('active');
  
  // Update property grid states
  propertyGrids.forEach(grid => {
    grid.classList.remove('active');
  });
  document.getElementById(`${targetType}-properties`).classList.add('active');
}

function handleFilterToggle(e) {
  // Toggle filter pill state
  const parentFilters = e.target.parentElement;
  const filterPillsInGroup = parentFilters.querySelectorAll('.filter-pill');
  
  filterPillsInGroup.forEach(pill => pill.classList.remove('active'));
  e.target.classList.add('active');
  
  // Apply filter logic here if needed
  renderProperties();
}

function handleSearch(e) {
  e.preventDefault();

  // Get search parameters
  const isShortTerm = document.querySelector('#short-term-search').classList.contains('active');
  const searchParams = getSearchParameters(isShortTerm);

  // If we are on a page without results, redirect to the properties page
  if (!document.getElementById('properties')) {
    redirectToProperties(searchParams, isShortTerm);
    return;
  }

  const filteredProperties = filterProperties(searchParams, isShortTerm);
  renderFilteredProperties(filteredProperties, isShortTerm);

  document.getElementById('properties').scrollIntoView({ behavior: 'smooth' });
}

function redirectToProperties(params, isShortTerm) {
  const query = new URLSearchParams();
  query.set('mode', isShortTerm ? 'short' : 'long');
  Object.keys(params).forEach(key => query.set(key, params[key]));
  query.set('adults', adults);
  query.set('children', children);
  window.location.href = `/luxury/properties/?${query.toString()}`;
}

function getSearchParameters(isShortTerm) {
  if (isShortTerm) {
    return {
      location: document.getElementById('location-short').value,
      checkin: document.getElementById('checkin').value,
      checkout: document.getElementById('checkout').value,
      guests: parseInt(document.getElementById('guests').value)
    };
  } else {
    return {
      location: document.getElementById('location-long').value,
      movein: document.getElementById('movein').value,
      lease: document.getElementById('lease').value,
      budget: document.getElementById('budget').value
    };
  }
}

function filterProperties(params, isShortTerm) {
  const properties = isShortTerm ? appData.shortTermProperties : appData.longTermProperties;
  
  return properties.filter(property => {
    // Location filter
    if (params.location && params.location !== '' && property.location !== params.location) {
      return false;
    }
    
    if (isShortTerm) {
      // Guest filter for short-term
      if (params.guests && property.guests < params.guests) {
        return false;
      }
    } else {
      // Budget filter for long-term
      if (params.budget && params.budget !== 'flexible') {
        const [min, max] = params.budget.split('-').map(val => {
          if (val.includes('+')) return parseInt(val.replace('+', ''));
          return parseInt(val);
        });
        
        if (max && (property.rent < min || property.rent > max)) {
          return false;
        } else if (!max && property.rent < min) {
          return false;
        }
      }
    }
    
    return true;
  });
}

function renderFilteredProperties(properties, isShortTerm) {
  const gridId = isShortTerm ? 'short-term-properties' : 'long-term-properties';
  const grid = document.getElementById(gridId);
  if (!grid) return;

  if (properties.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--color-text-muted); padding: 3rem;">No properties found matching your criteria.</div>';
    return;
  }
  
  grid.innerHTML = properties.map(property => 
    isShortTerm ? createShortTermPropertyCard(property) : createLongTermPropertyCard(property)
  ).join('');
}

function renderProperties() {
  renderShortTermProperties();
  renderLongTermProperties();
}

function renderShortTermProperties() {
  const grid = document.getElementById('short-term-properties');
  if (!grid) return;
  grid.innerHTML = appData.shortTermProperties.map(createShortTermPropertyCard).join('');
}

function renderLongTermProperties() {
  const grid = document.getElementById('long-term-properties');
  if (!grid) return;
  grid.innerHTML = appData.longTermProperties.map(createLongTermPropertyCard).join('');
}

function createShortTermPropertyCard(property) {
  return `
    <div class="property-card" data-property-id="${property.id}">
      <img src="${property.image}" alt="${property.title}" class="property-image">
      <div class="property-content">
        <h3 class="property-title">${property.title}</h3>
        <p class="property-location">${property.location}</p>
        <div class="property-price">$${property.price}/night</div>
        <div class="property-features">
          ${property.features.slice(0, 3).map(feature => `<span class="feature-tag">${feature}</span>`).join('')}
        </div>
        <div class="property-details">
          <span>${property.bedrooms} bed • ${property.bathrooms} bath • ${property.guests} guests</span>
          <span class="property-rating">★ ${property.rating}</span>
        </div>
      </div>
    </div>
  `;
}

function createLongTermPropertyCard(property) {
  return `
    <div class="property-card" data-property-id="${property.id}">
      <img src="${property.image}" alt="${property.title}" class="property-image">
      <div class="property-content">
        <h3 class="property-title">${property.title}</h3>
        <p class="property-location">${property.location}</p>
        <div class="property-price">$${property.rent.toLocaleString()}/month</div>
        <div class="property-features">
          ${property.features.slice(0, 3).map(feature => `<span class="feature-tag">${feature}</span>`).join('')}
        </div>
        <div class="property-details">
          <span>${property.bedrooms} bed • ${property.bathrooms} bath • ${property.sqft} sqft</span>
          <span class="property-rating">${property.furnished ? 'Furnished' : 'Unfurnished'}</span>
        </div>
        <div style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--color-text-muted);">
          Available: ${property.available} • ${property.lease}
        </div>
      </div>
    </div>
  `;
}

function handleSmoothScroll(e) {
  const targetId = e.target.getAttribute('href');
  // Only intercept anchor links on the same page
  if (targetId && targetId.startsWith('#')) {
    e.preventDefault();
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }
}

// Property card click handlers
document.addEventListener('click', function(e) {
  const propertyCard = e.target.closest('.property-card');
  if (propertyCard) {
    const propertyId = propertyCard.dataset.propertyId;
    handlePropertyCardClick(propertyId);
  }
});

function handlePropertyCardClick(propertyId) {
  // Add a subtle animation to indicate interaction
  const card = document.querySelector(`[data-property-id="${propertyId}"]`);
  card.style.transform = 'scale(0.98)';
  setTimeout(() => {
    card.style.transform = '';
  }, 150);
  
  // In a real application, this would navigate to a property details page
  console.log(`Property ${propertyId} clicked - would navigate to details page`);
}

// Add luxury hover effects to cards
document.addEventListener('mouseenter', function(e) {
  if (e.target.closest('.property-card, .team-card, .payment-card')) {
    e.target.closest('.property-card, .team-card, .payment-card').style.transform = 'translateY(-10px)';
  }
}, true);

document.addEventListener('mouseleave', function(e) {
  if (e.target.closest('.property-card, .team-card, .payment-card')) {
    e.target.closest('.property-card, .team-card, .payment-card').style.transform = '';
  }
}, true);

// Search input enhancements
document.querySelectorAll('.search-input').forEach(input => {
  input.addEventListener('focus', function() {
    this.parentElement.style.background = 'var(--color-surface-alt)';
    this.parentElement.style.boxShadow = '0 0 0 2px var(--color-primary)';
  });
  
  input.addEventListener('blur', function() {
    this.parentElement.style.background = '';
    this.parentElement.style.boxShadow = '';
  });
});

// Add loading animation for search
function showSearchLoading(isShortTerm) {
  const gridId = isShortTerm ? 'short-term-properties' : 'long-term-properties';
  const grid = document.getElementById(gridId);
  
  grid.innerHTML = `
    <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
      <div style="color: var(--color-primary); font-size: 1.2rem;">
        ✨ Searching luxury properties...
      </div>
    </div>
  `;
  
  // Simulate loading delay for better UX
  setTimeout(() => {
    renderProperties();
  }, 500);
}

// Initialize luxury animations
function initLuxuryAnimations() {
  // Add entrance animations to cards when they come into view
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);
  
  // Observe all cards for entrance animations
  document.querySelectorAll('.property-card, .team-card, .payment-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
  });
}

// Call luxury animations after a short delay
setTimeout(initLuxuryAnimations, 1000);
