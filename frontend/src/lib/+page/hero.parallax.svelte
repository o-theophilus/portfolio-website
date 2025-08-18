<script>
	import { Icon } from '$lib/macro';

	let scrollY;
</script>

<svelte:window bind:scrollY />

<section style:--scroll={scrollY}>
	<img style:--no="8" src="/parallax/parallax0.png" alt="parallax0" />
	<img style:--no="7" src="/parallax/parallax1.png" alt="parallax1" />

	<div class="block" style:--no="8">
		<div class="icon">
			<Icon icon="logo" size="96" />
		</div>
		<div class="details">
			<div class="name">Theophilus Ogbolu</div>
			<div class="role">Designer & Developer</div>
		</div>
	</div>

	<img style:--no="6" src="/parallax/parallax2.png" alt="parallax2" />
	<img style:--no="5" src="/parallax/parallax3.png" alt="parallax3" />
	<img style:--no="4" src="/parallax/parallax4.png" alt="parallax4" />
	<img style:--no="3" src="/parallax/parallax5.png" alt="parallax5" />
	<img style:--no="2" src="/parallax/parallax6.png" alt="parallax6" />
	<img style:--no="1" src="/parallax/parallax7.png" alt="parallax7" />
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
		outline: 10px solid #82c6ff;
		position: absolute;

		height: 100%;
		width: 100%;
		object-fit: cover;
		top: calc(0.1px * var(--no) * var(--scroll));
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
