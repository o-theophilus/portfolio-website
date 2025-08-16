<script>
	import {
		createIcons,
		Sun,
		Moon,
		ArrowDown,
		ArrowRight,
		ArrowLeft,
		ChevronLeft,
		ChevronRight,
		SquarePen,
		Mail,
		Phone,
		MapPin,
		SquareChevronUp,
		KeyRound,
		Eye,
		MessageCircle,
		ThumbsUp,
		Star,
		Share2,
		User,
		X,
		ChevronUp,
		ChevronDown,
		Save,
		History,
		SendHorizontal,
		Plus,
		LogOut,
		Search,
		EyeOff,
		ThumbsDown,
		MessageCirclePlus,
		Trash2,
		TriangleAlert,
		CircleX,
		SquareCheck,
		ArrowDownNarrowWide,
		Reply,
		Ellipsis
	} from 'lucide';
	import { onMount } from 'svelte';
	onMount(() => {
		createIcons({
			icons: {
				Sun,
				Moon,
				ArrowDown,
				ArrowRight,
				ArrowLeft,
				ChevronLeft,
				ChevronRight,
				SquarePen,
				Mail,
				Phone,
				MapPin,
				SquareChevronUp,
				KeyRound,
				Eye,
				MessageCircle,
				ThumbsUp,
				Star,
				Share2,
				User,
				X,
				ChevronUp,
				ChevronDown,
				Save,
				History,
				SendHorizontal,
				Plus,
				LogOut,
				Search,
				EyeOff,
				ThumbsDown,
				MessageCirclePlus,
				Trash2,
				TriangleAlert,
				CircleX,
				SquareCheck,
				ArrowDownNarrowWide,
				Reply,
				Ellipsis
			},
			attrs: {
				width: 16,
				height: 16,
				'stroke-width': 2.5
			},
			nameAttr: 'data-lucide'
		});
	});

	let { icon, size = 16 } = $props();
</script>

<svg data-lucide={icon} style:--size="{size}px"></svg>

<style>
	svg {
		width: var(--size);
		height: var(--size);
	}
</style>
