<script>
	let { active = true, size = 50 } = $props();
</script>

{#if active}
	<div class="circle" style:--size="{size}px">
		<div class="sector"></div>
		<div class=" sector v2"></div>
		<div class="center"></div>
	</div>
{/if}

<style>
	.circle {
		position: relative;

		--thickness: 8px;
		display: flex;
		justify-content: center;
		align-items: center;

		background-color: var(--cl1_t);
		background-color: var(--bg2);

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		overflow: hidden;
	}

	.center {
		position: relative;
		background-color: var(--bg1);

		width: calc(var(--size) * (1 / 3) * 2);
		height: calc(var(--size) * (1 / 3) * 2);
		border-radius: 50%;
	}

	.sector {
		position: absolute;
		left: 50%;
		top: 50%;

		background-color: var(--cl1);

		width: var(--size);
		height: var(--size);

		transform-origin: 0 0;
		animation: rotation 1s infinite linear;
	}

	.v2 {
		animation-duration: 2s;
	}

	@keyframes rotation {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(359deg);
		}
	}
</style>
