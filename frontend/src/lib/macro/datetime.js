// lib/date.js

// ---- formatters (created once) ----
const timeFormatter = new Intl.DateTimeFormat('en-GB', {
	hour: 'numeric',
	minute: '2-digit',
	hour12: true
});

const weekdayShort = new Intl.DateTimeFormat('en-GB', { weekday: 'short' });
const weekdayLong = new Intl.DateTimeFormat('en-GB', { weekday: 'long' });
const monthShort = new Intl.DateTimeFormat('en-GB', { month: 'short' });
const monthLong = new Intl.DateTimeFormat('en-GB', { month: 'long' });

const fullDate = new Intl.DateTimeFormat('en-GB', {
	day: 'numeric',
	month: 'numeric',
	year: 'numeric'
});

const fullDateTime = new Intl.DateTimeFormat('en-GB', {
	day: 'numeric',
	month: 'numeric',
	year: 'numeric',
	hour: 'numeric',
	minute: '2-digit',
	hour12: true
});

// ---- helpers ----
const ordinal = (n) => {
	const j = n % 10,
		k = n % 100;
	if (j === 1 && k !== 11) return `${n}st`;
	if (j === 2 && k !== 12) return `${n}nd`;
	if (j === 3 && k !== 13) return `${n}rd`;
	return `${n}th`;
};

export const formatTime = (date) => timeFormatter.format(date);

export const formatDate = (date, type) => {
	const day = date.getDate();
	const year = date.getFullYear();
	const hours = date.getHours();

	switch (type) {
		case 'day_short':
			return weekdayShort.format(date);
		case 'day_full':
			return weekdayLong.format(date);
		case 'month_short':
			return monthShort.format(date);
		case 'month_full':
			return monthLong.format(date);
		case 'date_ordinal':
			return `${ordinal(day)} of ${monthLong.format(date)} ${year}`;
		case 'date_numeric':
			return fullDate.format(date);
		case 'date_medium':
			return `${String(day).padStart(2, '0')} ${monthLong.format(date)} ${year}`;
		case 'date_named':
			return `${String(day).padStart(2, '0')}-${monthShort.format(date)}-${year}`;
		case 'time_period':
			return hours < 12 ? 'Morning' : hours < 16 ? 'Afternoon' : 'Evening';
		case 'time_12h':
			return formatTime(date);
		case 'year':
			return String(year);
		default:
			return date.toString();
	}
};

export const formatTimeAgo = (date, now = Date.now()) => {
	const diffMs = now - date.getTime();
	const diffMin = Math.floor(diffMs / 60000);
	const diffHr = diffMin / 60;

	if (diffMin < 1) return 'just now';
	if (diffMin < 60) return `${diffMin}m ago`;

	const today = new Date();
	const yesterday = new Date(today);
	yesterday.setDate(today.getDate() - 1);

	if (date.toDateString() === today.toDateString()) {
		return formatTime(date);
	}

	if (date.toDateString() === yesterday.toDateString()) {
		return `Yesterday ${formatTime(date)}`;
	}

	if (diffHr < 24 * 7) {
		return `${weekdayShort.format(date)} ${formatTime(date)}`;
	}

	return `${fullDate.format(date)} ${formatTime(date)}`;
};

export const needsLiveUpdates = (date, now = Date.now()) =>
	now - date.getTime() < 7 * 24 * 60 * 60 * 1000;

export const formatFullDateTime = (date) =>
	fullDateTime.format(date);
