<div class="block">
	<div class="pos">
		<div class="slider">
			<span class="text"> ART. CODE. DESIGN.&nbsp; </span>
			<span class="text"> ART. CODE. DESIGN.&nbsp; </span>
			<span class="text"> ART. CODE. DESIGN.&nbsp; </span>
			<span class="text"> ART. CODE. DESIGN.&nbsp; </span>
		</div>
	</div>
</div>

<style>
	.block {
		position: relative;
	}
	.pos {
		position: absolute;
		width: 100%;
		overflow: hidden;
	}

	@keyframes block {
		from {
			transform: translateX(0);
		}
		to {
			transform: translateX(-25%);
		}
	}

	.slider {
		width: fit-content;
		--speed: 40s;
		display: flex;
		animation: block var(--speed) linear infinite;
	}

	.text {
		white-space: nowrap;
		font-size: 10rem;
		font-weight: 600;
		line-height: 80%;

		background-image: linear-gradient(
			color-mix(in srgb, var(--ft2), transparent 80%),
			color-mix(in srgb, var(--ft2), transparent 98%)
		);
		background-clip: text;
		color: transparent;
	}

	@media screen and (min-width: 600px) {
		.text {
			font-size: 15rem;
		}
	}
</style>
