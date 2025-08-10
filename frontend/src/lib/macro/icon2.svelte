<script>
	import { Skull } from '@lucide/svelte';
	let { icon, size = 16 } = $props();
</script>

{#if icon == 'chevron-down'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m6 9 6 6 6-6" />
	</svg>
{:else if icon == 'chevron-up'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m18 15-6-6-6 6" />
	</svg>
{:else if icon == 'chevron-left'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m15 18-6-6 6-6" /></svg
	>
{:else if icon == 'chevron-right'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m9 18 6-6-6-6" /></svg
	>
{:else if icon == 'chevrons-right'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m6 17 5-5-5-5" /><path d="m13 17 5-5-5-5" /></svg
	>
{:else if icon == 'square-chevron-up'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<rect width="18" height="18" x="3" y="3" rx="2" /><path d="m8 14 4-4 4 4" /></svg
	>
{:else if icon == 'arrow_down'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="M12 5v14" />
		<path d="m19 12-7 7-7-7" />
	</svg>
{:else if icon == 'arrow_left'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m12 19-7-7 7-7" />
		<path d="M19 12H5" />
	</svg>
{:else if icon == 'arrow_right'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="M5 12h14" />
		<path d="m12 5 7 7-7 7" />
	</svg>
{:else if icon == 'send'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z" />
	</svg>
{:else if icon == 'light_mode'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<circle cx="12" cy="12" r="4" />
		<path d="M12 2v2" />
		<path d="M12 20v2" />
		<path d="m4.93 4.93 1.41 1.41" />
		<path d="m17.66 17.66 1.41 1.41" />
		<path d="M2 12h2" />
		<path d="M20 12h2" />
		<path d="m6.34 17.66-1.41 1.41" />
		<path d="m19.07 4.93-1.41 1.41" />
	</svg>
{:else if icon == 'dark_mode'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path
			d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"
		/>
	</svg>
{:else if icon == 'call'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path
			d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"
		/>
	</svg>
{:else if icon == 'email'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7" />
		<rect x="2" y="4" width="20" height="16" rx="2" />
	</svg>
{:else if icon == 'location'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path
			d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"
		/>
		<circle cx="12" cy="10" r="3" />
	</svg>
{:else if icon == 'x'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="M18 6 6 18" />
		<path d="m6 6 12 12" />
	</svg>
{:else if icon == '200'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<rect width="18" height="18" x="3" y="3" rx="2" />
		<path d="m9 12 2 2 4-4" />
	</svg>
{:else if icon == '201'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" />
		<path d="M12 9v4" />
		<path d="M12 17h.01" />
	</svg>
{:else if icon == '400'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<circle cx="12" cy="12" r="10" />
		<path d="m15 9-6 6" />
		<path d="m9 9 6 6" />
	</svg>
{:else if icon == 'search'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="m21 21-4.34-4.34" />
		<circle cx="11" cy="11" r="8" />
	</svg>
{:else if icon == 'edit'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
		<path
			d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"
		/>
	</svg>
{:else if icon == 'add'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="M5 12h14" />
		<path d="M12 5v14" />
	</svg>
{:else if icon == 'delete'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path d="M10 11v6" />
		<path d="M14 11v6" />
		<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" />
		<path d="M3 6h18" />
		<path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
	</svg>
{:else if icon == 'eye'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path
			d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"
		/>
		<circle cx="12" cy="12" r="3" />
	</svg>
{:else if icon == 'eye_off'}
	<svg width="{size}px" height="{size}px" viewBox="0 0 24 24" class="lucide">
		<path
			d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"
		/>
		<path d="M14.084 14.158a3 3 0 0 1-4.242-4.242" />
		<path
			d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"
		/>
		<path d="m2 2 20 20" />
	</svg>
{/if}

<style>
	svg.lucide {
		flex-shrink: 0;
		fill: none;
		stroke: currentColor;
		stroke-width: 2.5;
		stroke-linejoin: round;
		stroke-linecap: round;
	}
</style>
