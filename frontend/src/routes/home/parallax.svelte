<script>
	let scrollY;
	let speed = 0.1;
</script>

<section>
	<img style:top="{scrollY * speed * 8}px" src="/site/parallax/parallax0.png" alt="parallax0" />
	<img style:top="{scrollY * speed * 7}px" src="/site/parallax/parallax1.png" alt="parallax1" />
	<img style:top="{scrollY * speed * 6}px" src="/site/parallax/parallax2.png" alt="parallax2" />
	<img style:top="{scrollY * speed * 5}px" src="/site/parallax/parallax3.png" alt="parallax3" />
	<img style:top="{scrollY * speed * 4}px" src="/site/parallax/parallax4.png" alt="parallax4" />
	<img style:top="{scrollY * speed * 3}px" src="/site/parallax/parallax5.png" alt="parallax5" />
	<img style:top="{scrollY * speed * 2}px" src="/site/parallax/parallax6.png" alt="parallax6" />
	<img style:top="{scrollY * speed * 1}px" src="/site/parallax/parallax7.png" alt="parallax7" />
</section>

<svelte:window bind:scrollY />

<style>
	section {
		--speed: 0.1;

		position: relative;
		height: calc(100vh - var(--headerHeight));
		min-height: 800px;

		background-color: #ffaf1b;

		mask-image: url('/site/parallax/parallax8.png');
		mask-repeat: no-repeat;
		mask-size: cover;
		mask-position: center;
		-webkit-mask-image: url('/site/parallax/parallax8.png');
		-webkit-mask-repeat: no-repeat;
		-webkit-mask-size: cover;
		-webkit-mask-position: center;
	}
	img {
		position: absolute;

		border-radius: 0;

		height: 100%;
		object-fit: cover;
	}
</style>
