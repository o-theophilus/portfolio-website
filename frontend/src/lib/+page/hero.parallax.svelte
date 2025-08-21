<script>
	import { Icon } from '$lib/macro';

	let scrollY = $state(0);

	let _8 = $derived(0.1 * 8 * scrollY);
	let _7 = $derived(0.1 * 7 * scrollY);
	let _6 = $derived(0.1 * 6 * scrollY);
	let _5 = $derived(0.1 * 5 * scrollY);
	let _4 = $derived(0.1 * 4 * scrollY);
	let _3 = $derived(0.1 * 3 * scrollY);
	let _2 = $derived(0.1 * 2 * scrollY);
	let _1 = $derived(0.1 * 1 * scrollY);
</script>

<svelte:window bind:scrollY />

<section style:--scroll={scrollY}>
	<img
		style:transform="translateY({_8}px)"
		src="/parallax/parallax0.png"
		loading="lazy"
		alt="parallax0"
	/>
	<img
		style:transform="translateY({_7}px)"
		src="/parallax/parallax1.png"
		loading="lazy"
		alt="parallax1"
	/>

	<div class="block">
		<div class="icon">
			<Icon icon="logo" size="96" />
		</div>
		<div class="details">
			<div class="name">Theophilus Ogbolu</div>
			<div class="role">Designer & Developer</div>
		</div>
	</div>

	<img
		style:transform="translateY({_6}px)"
		src="/parallax/parallax2.png"
		loading="lazy"
		alt="parallax2"
	/>
	<img
		style:transform="translateY({_5}px)"
		src="/parallax/parallax3.png"
		loading="lazy"
		alt="parallax3"
	/>
	<img
		style:transform="translateY({_4}px)"
		src="/parallax/parallax4.png"
		loading="lazy"
		alt="parallax4"
	/>
	<img
		style:transform="translateY({_3}px)"
		src="/parallax/parallax5.png"
		loading="lazy"
		alt="parallax5"
	/>
	<img
		style:transform="translateY({_2}px)"
		src="/parallax/parallax6.png"
		loading="lazy"
		alt="parallax6"
	/>
	<img
		style:transform="translateY({_1}px)"
		src="/parallax/parallax7.png"
		loading="lazy"
		alt="parallax7"
	/>
</section>

<style>
	section {
		position: relative;
		height: calc(100vh - var(--headerHeight));
		min-height: 500px;

		background-color: #82c6ff;

		mask-image: url('/parallax/parallax8.png');
		mask-repeat: no-repeat;
		mask-size: cover;
		mask-position: center;
		-webkit-mask-image: url('/parallax/parallax8.png');
		-webkit-mask-repeat: no-repeat;
		-webkit-mask-size: cover;
		-webkit-mask-position: center;
	}

	img {
		position: absolute;

		height: 100%;
		width: 100%;
		object-fit: cover;
	}

	.block {
		position: fixed;
		top: 100px;

		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--sp2);

		width: 100%;
		padding: var(--sp2);

		color: var(--bg1);
		transition: color var(--trans);
	}

	.details {
		display: flex;
		flex-direction: column;
		text-align: center;
	}

	@media screen and (min-height: 600px) {
		.block {
			flex-direction: column;
			top: 140px;
		}
		.details {
			align-items: center;
		}
	}

	.icon {
		border-radius: 50%;
		line-height: 0;
		fill: var(--cl1);
		background-color: white;
	}

	.name {
		font-size: 2rem;
		font-weight: 800;
	}

	.role {
		font-size: 1.1rem;
	}
</style>
