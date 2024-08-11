<script>
	import Icon from '$lib/icon.svelte';

	let scrollY;
</script>

<svelte:window bind:scrollY />

<section>
	<img style:--top="{scrollY}px" style:--no="8" src="/parallax/parallax0.png" alt="parallax0" />
	<div class="block" style:--top="{scrollY}px" style:--no="8">
		<div class="icon">
			<Icon icon="logo" size="6" />
		</div>
		<div class="name">Theophilus Ogbolu</div>
		<div class="role">Designer & Developer</div>
	</div>
	<img style:--top="{scrollY}px" style:--no="7" src="/parallax/parallax1.png" alt="parallax1" />
	<img style:--top="{scrollY}px" style:--no="6" src="/parallax/parallax2.png" alt="parallax2" />
	<img style:--top="{scrollY}px" style:--no="5" src="/parallax/parallax3.png" alt="parallax3" />
	<img style:--top="{scrollY}px" style:--no="4" src="/parallax/parallax4.png" alt="parallax4" />
	<img style:--top="{scrollY}px" style:--no="3" src="/parallax/parallax5.png" alt="parallax5" />
	<img style:--top="{scrollY}px" style:--no="2" src="/parallax/parallax6.png" alt="parallax6" />
	<img style:--top="{scrollY}px" style:--no="1" src="/parallax/parallax7.png" alt="parallax7" />
</section>

<style>
	section {
		position: relative;
		height: calc(100vh - var(--headerHeight));
		min-height: 800px;

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

	img,
	.block {
		position: absolute;

		height: 100%;
		width: 100%;
		object-fit: cover;
		transform: translateY(calc(0.1 * var(--no) * var(--top)));
		/* top: calc(0.1 * var(--no) * var(--top)); */
	}

	.block {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		height: 50%;
		padding: var(--sp2);

		color: var(--bg1);
		transition: color var(--trans);
	}

	.icon {
		color: var(--cl1);
	}

	.name {
		font-size: 2rem;
		font-weight: 800;
		text-align: center;
	}

	.role {
		font-size: 1.1rem;
	}
</style>
