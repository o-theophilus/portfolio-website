<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { loading, notify, module, app } from '$lib/store.svelte.js';

	import { Button, RoundButton } from '$lib/button';
	import { Icon } from '$lib/macro';

	let { ops, onadd } = $props();
	let files = $derived(ops.files);

	const order = (dir = true) => {
		ops.error = {};

		if (files.length < 2 || !ops.active) return;
		const currentIndex = files.indexOf(ops.active);

		if (currentIndex == -1) return;
		const newIndex = dir ? currentIndex + 1 : currentIndex - 1;
		if (newIndex < 0 || newIndex >= files.length) return;

		files = files.map((file, i) => {
			if (i === currentIndex) return files[newIndex];
			if (i === newIndex) return files[currentIndex];
			return file;
		});
	};

	const remove = () => {
		ops.error = {};

		let i = files.findIndex((x) => x == ops.active);
		files = files.filter((x) => x != ops.active);

		if (i < files.length) {
			ops.active = files[i];
		} else if (i == files.length) {
			ops.active = files[i - 1];
		} else {
			ops.active = files[0];
		}
	};

	const submit = async () => {
		ops.error = {};

		loading.open('Saving . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/file/${ops.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ files })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			ops.files = resp.item.files;
			module.value.update(resp.item);
			notify.open('Order Saved');
		} else {
			ops.error = resp;
		}
	};
</script>

<div class="line">
	{#each files as x, i (x)}
		<div
			class="used"
			animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
			class:excess={i > ops.count - 1}
			class:active={ops.active == x}
			onclick={() => {
				ops.error = {};
				ops.active = x;
			}}
			role="presentation"
		>
			{#if x.slice(-4) == '.jpg'}
				<img src="{x}/200" alt={ops.title} onerror={(e) => (e.target.src = '/file_error.png')} />
			{:else}
				{x.slice(-3)}
			{/if}
		</div>
	{/each}

	{#if ops.count - files.length > 0}
		{#each Array(ops.count - files.length) as _, i (i)}
			<div
				class="empty"
				animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
				onclick={() => {
					if (ops.files.length < ops.count) {
						onadd();
					} else {
						ops.error.error = 'save changes and try again';
					}
				}}
				role="presentation"
			>
				<Icon icon="plus" />
			</div>
		{/each}
	{/if}
</div>

<div class="line">
	<RoundButton
		icon="chevron-left"
		disabled={files.length <= 1 || files[0] == ops.active}
		onclick={() => {
			order(false);
		}}
	/>

	<RoundButton
		icon="chevron-right"
		disabled={files.length <= 1 || files[files.length - 1] == ops.active}
		onclick={order}
	/>

	<RoundButton icon="trash-2" disabled={files.length == 0} onclick={remove} />
</div>

<br />

<div class="line">
	<Button
		icon="save"
		disabled={JSON.stringify(ops.files) == JSON.stringify(files)}
		onclick={submit}
	>
		Save
	</Button>

	<Button
		icon="history"
		onclick={() => {
			ops.error = {};
			files = ops.files;
			if (!files.includes(ops.active)) ops.active = files[0];
		}}
		disabled={JSON.stringify(ops.files) == JSON.stringify(files)}
	>
		Reset
	</Button>
</div>

<style>
	.line {
		--size: 50px;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);
		flex-wrap: wrap;
		margin-top: var(--sp2);
	}

	.used,
	.empty {
		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: var(--sp0);
		cursor: pointer;
		overflow: hidden;
		font-size: 0.8rem;

		background-color: var(--bg2);
		outline: 2px solid transparent;
		transition:
			outline-color var(--trans),
			transform var(--trans);
	}

	.used:hover,
	.empty:hover {
		outline-color: var(--cl1);
	}

	.excess {
		outline-color: red;
		opacity: 0.5;
	}

	.active {
		outline-color: var(--cl1);
		transform: scale(1.1);
	}

	img {
		width: 100%;
	}
</style>
