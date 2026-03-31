#!/usr/bin/env python3
"""
build_phase_5b.py
=================
Phase 5B: Personas System
AI Chat Platform - Professional Multi-Platform AI Chat with Personas
"""

import os
import sys

def create_file(path: str, content: str) -> None:
    """Create a file with the given path and content, creating directories as needed."""
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Created: {path}")

def main():
    print("=" * 60)
    print("🚀 Phase 5B: Personas System")
    print("=" * 60)

    files_created = 0

    # ──────────────────────────────────────────────
    # 1. hooks/usePersonas.ts
    # ──────────────────────────────────────────────
    print("\n📦 Hooks")

    create_file("hooks/usePersonas.ts", '''// هوك الشخصيات - جلب وإنشاء وتعديل وحذف ومشاركة وتقييم ونسخ وتجربة
"use client";

import { useState, useCallback, useEffect, useRef } from "react";

import { getSupabaseBrowser } from "@/lib/supabase-client";
import { useAuthStore } from "@/stores/authStore";
import { usePersonaStore } from "@/stores/personaStore";
import { FREE_MAX_PERSONAS } from "@/utils/constants";

import type {
  Persona,
  PersonaCategory,
  PersonaType,
  CreatePersonaData,
  UpdatePersonaData,
  PersonaRating,
  PremiumPersonaTrial,
} from "@/types/persona";

/**
 * القيم المُرجعة من هوك الشخصيات
 */
interface UsePersonasReturn {
  personas: Persona[];
  systemPersonas: Persona[];
  premiumPersonas: Persona[];
  customPersonas: Persona[];
  communityPersonas: Persona[];
  activePersona: Persona | null;
  isLoading: boolean;
  customCount: number;
  canCreateCustom: boolean;
  fetchPersonas: () => Promise<void>;
  setActive: (persona: Persona | null) => void;
  clearActive: () => void;
  createPersona: (data: CreatePersonaData) => Promise<Persona | null>;
  updatePersona: (id: string, data: UpdatePersonaData) => Promise<boolean>;
  deletePersona: (id: string) => Promise<boolean>;
  sharePersona: (id: string) => Promise<boolean>;
  ratePersona: (personaId: string, rating: number) => Promise<boolean>;
  getUserRating: (personaId: string) => Promise<number | null>;
  copyPersona: (persona: Persona) => Promise<Persona | null>;
  checkTrialUsed: (personaId: string) => Promise<boolean>;
  useTrialMessage: (personaId: string) => Promise<boolean>;
}

/**
 * هوك إدارة الشخصيات الكامل
 */
export function usePersonas(): UsePersonasReturn {
  const supabase = getSupabaseBrowser();
  const user = useAuthStore((s) => s.user);
  const role = useAuthStore((s) => s.role);
  const activePersona = usePersonaStore((s) => s.activePersona);
  const setActivePersona = usePersonaStore((s) => s.setActivePersona);
  const clearPersona = usePersonaStore((s) => s.clearPersona);

  const [personas, setPersonas] = useState<Persona[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const isMountedRef = useRef(true);

  /**
   * جلب جميع الشخصيات المتاحة
   */
  const fetchPersonas = useCallback(async () => {
    setIsLoading(true);
    try {
      const { data, error } = await supabase
        .from("personas")
        .select("*")
        .eq("is_active", true)
        .order("usage_count", { ascending: false });

      if (error) throw error;
      if (isMountedRef.current) {
        setPersonas((data as Persona[]) ?? []);
      }
    } catch {
      // صامت
    } finally {
      if (isMountedRef.current) setIsLoading(false);
    }
  }, [supabase]);

  /**
   * تعيين الشخصية النشطة
   */
  const setActive = useCallback(
    (persona: Persona | null) => {
      setActivePersona(persona);
    },
    [setActivePersona]
  );

  /**
   * مسح الشخصية النشطة
   */
  const clearActive = useCallback(() => {
    clearPersona();
  }, [clearPersona]);

  /**
   * إنشاء شخصية مخصصة جديدة
   */
  const createPersona = useCallback(
    async (data: CreatePersonaData): Promise<Persona | null> => {
      if (!user) return null;

      // التحقق من الحد للمستخدم المجاني
      if (role === "free") {
        const currentCustom = personas.filter(
          (p) => p.type === "custom" && p.user_id === user.id
        ).length;
        if (currentCustom >= FREE_MAX_PERSONAS) return null;
      }

      try {
        const { data: created, error } = await supabase
          .from("personas")
          .insert({
            user_id: user.id,
            name: data.name.trim(),
            description: data.description.trim(),
            system_prompt: data.system_prompt.trim(),
            icon_url: data.icon_url ?? null,
            category: data.category,
            type: data.type === "shared" ? "shared" : "custom",
            is_active: true,
            is_approved: false,
          })
          .select()
          .single();

        if (error) throw error;

        const newPersona = created as Persona;
        if (isMountedRef.current) {
          setPersonas((prev) => [newPersona, ...prev]);
        }

        // إشعار عند المشاركة
        if (data.type === "shared") {
          await supabase.from("notifications").insert({
            type: "persona_shared",
            title: "مشاركة شخصية جديدة",
            message: `قام ${user.email} بمشاركة شخصية: ${data.name}`,
            priority: "info",
            related_user_id: user.id,
            metadata: { persona_name: data.name, persona_id: newPersona.id },
          });
        }

        return newPersona;
      } catch {
        return null;
      }
    },
    [user, role, personas, supabase]
  );

  /**
   * تحديث شخصية
   */
  const updatePersona = useCallback(
    async (id: string, data: UpdatePersonaData): Promise<boolean> => {
      try {
        const updateData: Record<string, unknown> = {
          updated_at: new Date().toISOString(),
        };

        if (data.name !== undefined) updateData.name = data.name.trim();
        if (data.description !== undefined) updateData.description = data.description.trim();
        if (data.system_prompt !== undefined) updateData.system_prompt = data.system_prompt.trim();
        if (data.icon_url !== undefined) updateData.icon_url = data.icon_url;
        if (data.category !== undefined) updateData.category = data.category;
        if (data.is_active !== undefined) updateData.is_active = data.is_active;
        if (data.is_approved !== undefined) updateData.is_approved = data.is_approved;

        const { error } = await supabase
          .from("personas")
          .update(updateData)
          .eq("id", id);

        if (error) throw error;

        if (isMountedRef.current) {
          setPersonas((prev) =>
            prev.map((p) => (p.id === id ? { ...p, ...updateData } as Persona : p))
          );

          // تحديث الشخصية النشطة إذا كانت هي
          if (activePersona?.id === id) {
            setActivePersona({ ...activePersona, ...updateData } as Persona);
          }
        }
        return true;
      } catch {
        return false;
      }
    },
    [supabase, activePersona, setActivePersona]
  );

  /**
   * حذف شخصية
   */
  const deletePersona = useCallback(
    async (id: string): Promise<boolean> => {
      try {
        const { error } = await supabase
          .from("personas")
          .delete()
          .eq("id", id);

        if (error) throw error;

        if (isMountedRef.current) {
          setPersonas((prev) => prev.filter((p) => p.id !== id));
          if (activePersona?.id === id) {
            clearPersona();
          }
        }
        return true;
      } catch {
        return false;
      }
    },
    [supabase, activePersona, clearPersona]
  );

  /**
   * مشاركة شخصية مع المجتمع
   */
  const sharePersona = useCallback(
    async (id: string): Promise<boolean> => {
      if (!user) return false;
      try {
        const { error } = await supabase
          .from("personas")
          .update({
            type: "shared",
            is_approved: false,
            updated_at: new Date().toISOString(),
          })
          .eq("id", id)
          .eq("user_id", user.id);

        if (error) throw error;

        // إشعار
        const persona = personas.find((p) => p.id === id);
        if (persona) {
          await supabase.from("notifications").insert({
            type: "persona_shared",
            title: "مشاركة شخصية جديدة",
            message: `قام ${user.email} بمشاركة شخصية: ${persona.name}`,
            priority: "info",
            related_user_id: user.id,
            metadata: { persona_name: persona.name, persona_id: id },
          });
        }

        if (isMountedRef.current) {
          setPersonas((prev) =>
            prev.map((p) =>
              p.id === id ? { ...p, type: "shared" as PersonaType, is_approved: false } : p
            )
          );
        }
        return true;
      } catch {
        return false;
      }
    },
    [user, supabase, personas]
  );

  /**
   * تقييم شخصية (1-5)
   */
  const ratePersona = useCallback(
    async (personaId: string, rating: number): Promise<boolean> => {
      if (!user || rating < 1 || rating > 5) return false;

      try {
        // التحقق من تقييم سابق
        const { data: existing } = await supabase
          .from("persona_ratings")
          .select("id")
          .eq("persona_id", personaId)
          .eq("user_id", user.id)
          .single();

        if (existing) {
          // تحديث التقييم
          const { error } = await supabase
            .from("persona_ratings")
            .update({ rating })
            .eq("id", existing.id);

          if (error) throw error;
        } else {
          // إنشاء تقييم جديد
          const { error } = await supabase
            .from("persona_ratings")
            .insert({
              persona_id: personaId,
              user_id: user.id,
              rating,
            });

          if (error) throw error;
        }

        // إعادة جلب الشخصية المحدثة (المشغل يحدث المتوسط)
        const { data: updated } = await supabase
          .from("personas")
          .select("average_rating, rating_count")
          .eq("id", personaId)
          .single();

        if (updated && isMountedRef.current) {
          setPersonas((prev) =>
            prev.map((p) =>
              p.id === personaId
                ? {
                    ...p,
                    average_rating: updated.average_rating,
                    rating_count: updated.rating_count,
                  }
                : p
            )
          );
        }

        return true;
      } catch {
        return false;
      }
    },
    [user, supabase]
  );

  /**
   * جلب تقييم المستخدم لشخصية
   */
  const getUserRating = useCallback(
    async (personaId: string): Promise<number | null> => {
      if (!user) return null;

      try {
        const { data } = await supabase
          .from("persona_ratings")
          .select("rating")
          .eq("persona_id", personaId)
          .eq("user_id", user.id)
          .single();

        return data?.rating ?? null;
      } catch {
        return null;
      }
    },
    [user, supabase]
  );

  /**
   * نسخ شخصية كمخصصة
   */
  const copyPersona = useCallback(
    async (persona: Persona): Promise<Persona | null> => {
      return createPersona({
        name: `${persona.name} (نسخة)`,
        description: persona.description,
        system_prompt: persona.system_prompt,
        icon_url: persona.icon_url ?? undefined,
        category: persona.category as PersonaCategory,
        type: "custom",
      });
    },
    [createPersona]
  );

  /**
   * التحقق من استخدام التجربة المجانية لشخصية مميزة
   */
  const checkTrialUsed = useCallback(
    async (personaId: string): Promise<boolean> => {
      if (!user) return true;

      try {
        const { data } = await supabase
          .from("premium_persona_trials")
          .select("id")
          .eq("user_id", user.id)
          .eq("persona_id", personaId)
          .single();

        return !!data;
      } catch {
        return false;
      }
    },
    [user, supabase]
  );

  /**
   * استخدام رسالة تجريبية مجانية لشخصية مميزة
   */
  const useTrialMessage = useCallback(
    async (personaId: string): Promise<boolean> => {
      if (!user) return false;

      try {
        const { error } = await supabase
          .from("premium_persona_trials")
          .insert({
            user_id: user.id,
            persona_id: personaId,
          });

        if (error) {
          // خطأ unique constraint يعني تم الاستخدام مسبقاً
          if (error.code === "23505") return false;
          throw error;
        }

        return true;
      } catch {
        return false;
      }
    },
    [user, supabase]
  );

  // تصنيف الشخصيات
  const systemPersonas = personas.filter((p) => p.type === "system");
  const premiumPersonas = personas.filter((p) => p.type === "premium");
  const customPersonas = personas.filter(
    (p) => p.type === "custom" && p.user_id === user?.id
  );
  const communityPersonas = personas.filter(
    (p) => p.type === "shared" && p.is_approved
  );
  const customCount = customPersonas.length;
  const canCreateCustom = role !== "free" || customCount < FREE_MAX_PERSONAS;

  useEffect(() => {
    isMountedRef.current = true;
    fetchPersonas();
    return () => {
      isMountedRef.current = false;
    };
  }, [fetchPersonas]);

  return {
    personas,
    systemPersonas,
    premiumPersonas,
    customPersonas,
    communityPersonas,
    activePersona,
    isLoading,
    customCount,
    canCreateCustom,
    fetchPersonas,
    setActive,
    clearActive,
    createPersona,
    updatePersona,
    deletePersona,
    sharePersona,
    ratePersona,
    getUserRating,
    copyPersona,
    checkTrialUsed,
    useTrialMessage,
  };
}
''')
    files_created += 1

    # ──────────────────────────────────────────────
    # 2. app/[locale]/personas/page.tsx
    # ──────────────────────────────────────────────
    print("\n📦 Pages")

    create_file("app/[locale]/personas/page.tsx", '''// صفحة مكتبة الشخصيات - عرض جميع الشخصيات مع البحث والتصفية
"use client";

import { useTranslations } from "next-intl";

import RouteGuard from "@/components/auth/RouteGuard";
import Sidebar from "@/components/sidebar/Sidebar";
import PersonaLibrary from "@/components/personas/PersonaLibrary";
import { cn } from "@/utils/cn";

/**
 * المحتوى الداخلي لصفحة الشخصيات
 */
function PersonasPageContent() {
  const t = useTranslations("personas");

  return (
    <div className="flex h-screen overflow-hidden bg-light-bg dark:bg-dark-bg">
      <Sidebar />

      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* الرأس */}
        <header
          className={cn(
            "flex items-center justify-between",
            "px-6 py-4",
            "border-b border-gray-200 dark:border-dark-border",
            "bg-white dark:bg-dark-card"
          )}
        >
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
            {t("library_title")}
          </h1>
        </header>

        {/* المكتبة */}
        <div className="flex-1 overflow-y-auto">
          <PersonaLibrary />
        </div>
      </main>
    </div>
  );
}

/**
 * صفحة مكتبة الشخصيات - محمية
 */
export default function PersonasPage() {
  return (
    <RouteGuard>
      <PersonasPageContent />
    </RouteGuard>
  );
}
''')
    files_created += 1

    # ──────────────────────────────────────────────
    # 3. app/[locale]/personas/create/page.tsx
    # ──────────────────────────────────────────────
    create_file("app/[locale]/personas/create/page.tsx", '''// صفحة إنشاء شخصية جديدة - نموذج الإنشاء مع عداد الحد
"use client";

import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

import RouteGuard from "@/components/auth/RouteGuard";
import Sidebar from "@/components/sidebar/Sidebar";
import PersonaForm from "@/components/personas/PersonaForm";
import { usePersonas } from "@/hooks/usePersonas";
import { useAuthStore } from "@/stores/authStore";
import { useUIStore } from "@/stores/uiStore";
import { FREE_MAX_PERSONAS } from "@/utils/constants";
import { cn } from "@/utils/cn";

/**
 * المحتوى الداخلي لصفحة إنشاء شخصية
 */
function CreatePersonaContent() {
  const t = useTranslations("personas");
  const tCommon = useTranslations("common");
  const router = useRouter();
  const locale = useUIStore((s) => s.locale);
  const role = useAuthStore((s) => s.role);
  const { customCount, canCreateCustom } = usePersonas();

  return (
    <div className="flex h-screen overflow-hidden bg-light-bg dark:bg-dark-bg">
      <Sidebar />

      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* الرأس */}
        <header
          className={cn(
            "flex items-center justify-between",
            "px-6 py-4",
            "border-b border-gray-200 dark:border-dark-border",
            "bg-white dark:bg-dark-card"
          )}
        >
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push(`/${locale}/personas`)}
              aria-label={tCommon("back")}
              className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-hover transition-colors"
            >
              <ArrowRight className="h-5 w-5 text-gray-500 rtl-flip" />
            </button>
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              {t("create_title")}
            </h1>
          </div>

          {/* عداد الشخصيات للمجاني */}
          {role === "free" && (
            <span
              className={cn(
                "text-xs font-medium px-3 py-1 rounded-full",
                canCreateCustom
                  ? "bg-primary/10 text-primary"
                  : "bg-red-100 dark:bg-red-900/20 text-red-600 dark:text-red-400"
              )}
            >
              {t("persona_count", {
                count: customCount,
                max: FREE_MAX_PERSONAS,
              })}
            </span>
          )}
        </header>

        {/* المحتوى */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-2xl mx-auto">
            {canCreateCustom ? (
              <PersonaForm />
            ) : (
              <div className="text-center py-12 space-y-4">
                <p className="text-gray-500 dark:text-gray-400">
                  {t("at_limit_message")}
                </p>
                <button
                  onClick={() => router.push(`/${locale}/personas`)}
                  className={cn(
                    "px-4 py-2 rounded-lg",
                    "bg-primary hover:bg-primary-600 text-white text-sm font-medium",
                    "transition-colors"
                  )}
                >
                  {tCommon("back")}
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

/**
 * صفحة إنشاء شخصية - محمية
 */
export default function CreatePersonaPage() {
  return (
    <RouteGuard>
      <CreatePersonaContent />
    </RouteGuard>
  );
}
''')
    files_created += 1

    # ──────────────────────────────────────────────
    # 4-9. Persona Components
    # ──────────────────────────────────────────────
    print("\n📦 Persona Components")

    # 4. PersonaCard
    create_file("components/personas/PersonaCard.tsx", '''// بطاقة الشخصية - أيقونة واسم ووصف وتصنيف وتقييم مع أزرار التفاعل
"use client";

import { useState, useCallback, useEffect } from "react";
import { useTranslations } from "next-intl";
import { Star, Copy, Check, Lock, Sparkles } from "lucide-react";

import PersonaRating from "@/components/personas/PersonaRating";
import PremiumPersonaLock from "@/components/personas/PremiumPersonaLock";
import { usePersonas } from "@/hooks/usePersonas";
import { useFavorites } from "@/hooks/useFavorites";
import { useAuthStore } from "@/stores/authStore";
import { usePersonaStore } from "@/stores/personaStore";
import { PERSONA_CATEGORIES } from "@/utils/constants";
import { cn } from "@/utils/cn";

import type { Persona } from "@/types/persona";

/**
 * خصائص بطاقة الشخصية
 */
interface PersonaCardProps {
  persona: Persona;
  onUse?: (persona: Persona) => void;
}

/**
 * بطاقة عرض شخصية واحدة
 */
export default function PersonaCard({ persona, onUse }: PersonaCardProps) {
  const t = useTranslations("personas");
  const role = useAuthStore((s) => s.role);
  const activePersona = usePersonaStore((s) => s.activePersona);
  const { setActive, copyPersona } = usePersonas();
  const { isFavorited, addFavorite, removeFavorite } = useFavorites();

  const [isCopying, setIsCopying] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showLock, setShowLock] = useState(false);

  const isActive = activePersona?.id === persona.id;
  const isPremiumLocked = persona.type === "premium" && role === "free";
  const isShared = persona.type === "shared";
  const isFav = isFavorited("persona", persona.id);

  const categoryInfo = PERSONA_CATEGORIES.find(
    (c) => c.value === persona.category
  );

  /**
   * استخدام الشخصية
   */
  const handleUse = useCallback(() => {
    if (isPremiumLocked) {
      setShowLock(true);
      return;
    }

    if (isActive) {
      setActive(null);
    } else {
      setActive(persona);
    }

    if (onUse) {
      onUse(persona);
    }
  }, [isPremiumLocked, isActive, persona, setActive, onUse]);

  /**
   * نسخ الشخصية
   */
  const handleCopy = useCallback(async () => {
    setIsCopying(true);
    try {
      const result = await copyPersona(persona);
      if (result) {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch {
      // صامت
    } finally {
      setIsCopying(false);
    }
  }, [persona, copyPersona]);

  /**
   * تبديل المفضلة
   */
  const handleFavoriteToggle = useCallback(async () => {
    if (isFav) {
      await removeFavorite("persona", persona.id);
    } else {
      await addFavorite("persona", persona.id);
    }
  }, [isFav, persona.id, addFavorite, removeFavorite]);

  return (
    <>
      <div
        className={cn(
          "relative rounded-xl p-4",
          "bg-white dark:bg-dark-card",
          "border-2 transition-all duration-200",
          "hover:shadow-md dark:hover:shadow-lg",
          isActive
            ? "border-primary shadow-sm shadow-primary/10"
            : "border-gray-200 dark:border-dark-border hover:border-gray-300 dark:hover:border-gray-600"
        )}
      >
        {/* شارة النوع */}
        {persona.type === "premium" && (
          <div className="absolute top-2 end-2">
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 text-[10px] font-semibold">
              <Sparkles className="h-2.5 w-2.5" />
              Premium
            </span>
          </div>
        )}

        {/* الرأس: أيقونة + اسم + تصنيف */}
        <div className="flex items-start gap-3 mb-3">
          <div
            className={cn(
              "flex-shrink-0 h-12 w-12 rounded-xl",
              "bg-primary/10 dark:bg-primary/20",
              "flex items-center justify-center text-2xl"
            )}
          >
            {persona.icon_url ?? "🎭"}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-bold text-gray-900 dark:text-white truncate">
              {persona.name}
            </h3>
            {categoryInfo && (
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {categoryInfo.icon} {categoryInfo.labelAr}
              </span>
            )}
          </div>
        </div>

        {/* الوصف */}
        <p className="text-xs text-gray-600 dark:text-gray-300 line-clamp-2 mb-3 leading-relaxed">
          {persona.description}
        </p>

        {/* التقييم (للمشتركة فقط) */}
        {(isShared || persona.type === "premium") && persona.rating_count > 0 && (
          <div className="mb-3">
            <PersonaRating
              personaId={persona.id}
              averageRating={persona.average_rating}
              ratingCount={persona.rating_count}
              compact
            />
          </div>
        )}

        {/* الأزرار */}
        <div className="flex items-center gap-2">
          {/* زر الاستخدام */}
          <button
            onClick={handleUse}
            className={cn(
              "flex-1 flex items-center justify-center gap-1.5",
              "px-3 py-2 rounded-lg text-xs font-medium",
              "transition-colors",
              isActive
                ? "bg-primary text-white"
                : isPremiumLocked
                ? "bg-gray-100 dark:bg-dark-hover text-gray-500 dark:text-gray-400"
                : "bg-primary/10 text-primary hover:bg-primary/20"
            )}
          >
            {isPremiumLocked && <Lock className="h-3 w-3" />}
            <span>
              {isActive ? t("use_persona") : isPremiumLocked ? t("upgrade_prompt").slice(0, 15) + "..." : t("use_persona")}
            </span>
          </button>

          {/* نسخ (مجتمع/مميز) */}
          {(isShared || persona.type === "system") && (
            <button
              onClick={handleCopy}
              disabled={isCopying}
              aria-label={t("copy_persona")}
              className={cn(
                "p-2 rounded-lg transition-colors",
                "text-gray-400 hover:text-primary",
                "hover:bg-gray-100 dark:hover:bg-dark-hover",
                "disabled:opacity-50"
              )}
            >
              {copied ? (
                <Check className="h-4 w-4 text-green-500" />
              ) : (
                <Copy className="h-4 w-4" />
              )}
            </button>
          )}

          {/* المفضلة */}
          <button
            onClick={handleFavoriteToggle}
            aria-label="Toggle favorite"
            className={cn(
              "p-2 rounded-lg transition-colors",
              isFav
                ? "text-yellow-500"
                : "text-gray-400 hover:text-yellow-500",
              "hover:bg-gray-100 dark:hover:bg-dark-hover"
            )}
          >
            <Star
              className={cn("h-4 w-4", isFav && "fill-yellow-500")}
            />
          </button>
        </div>
      </div>

      {/* مكون القفل المميز */}
      {showLock && (
        <PremiumPersonaLock
          persona={persona}
          onClose={() => setShowLock(false)}
        />
      )}
    </>
  );
}
''')
    files_created += 1

    # 5. PersonaForm
    create_file("components/personas/PersonaForm.tsx", '''// نموذج إنشاء/تعديل شخصية - اسم ووصف وتصنيف وأيقونة وتعليمات مع معاينة
"use client";

import { useState, useCallback, useMemo } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { Save, Share2, Eye, Loader2 } from "lucide-react";

import PersonaPreview from "@/components/personas/PersonaPreview";
import { usePersonas } from "@/hooks/usePersonas";
import { useUIStore } from "@/stores/uiStore";
import { isValidSystemPrompt } from "@/utils/validators";
import { PERSONA_CATEGORIES, MAX_SYSTEM_PROMPT_LENGTH } from "@/utils/constants";
import { cn } from "@/utils/cn";

import type { Persona, PersonaCategory, CreatePersonaData } from "@/types/persona";

/**
 * خصائص نموذج الشخصية
 */
interface PersonaFormProps {
  editPersona?: Persona;
}

const EMOJI_OPTIONS = [
  "🎯", "💡", "🧠", "⚡", "🔥", "💼", "📚", "✍️",
  "🤖", "🎨", "📊", "🌐", "💻", "📧", "🔬", "📢",
  "🎓", "🌍", "🏆", "🎭", "🧪", "📝", "🔮", "🛠️",
];

/**
 * نموذج إنشاء أو تعديل شخصية
 */
export default function PersonaForm({ editPersona }: PersonaFormProps) {
  const t = useTranslations("personas");
  const tCommon = useTranslations("common");
  const router = useRouter();
  const locale = useUIStore((s) => s.locale);
  const { createPersona, updatePersona } = usePersonas();

  const [name, setName] = useState(editPersona?.name ?? "");
  const [description, setDescription] = useState(editPersona?.description ?? "");
  const [category, setCategory] = useState<PersonaCategory>(
    (editPersona?.category as PersonaCategory) ?? "general"
  );
  const [iconUrl, setIconUrl] = useState(editPersona?.icon_url ?? "🎯");
  const [systemPrompt, setSystemPrompt] = useState(editPersona?.system_prompt ?? "");
  const [showPreview, setShowPreview] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isSavingShared, setIsSavingShared] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);

  const isEditing = !!editPersona;
  const promptLength = systemPrompt.length;
  const isPromptValid = isValidSystemPrompt(systemPrompt);

  const isFormValid = useMemo(() => {
    return (
      name.trim().length >= 2 &&
      name.trim().length <= 100 &&
      description.trim().length >= 5 &&
      isPromptValid
    );
  }, [name, description, isPromptValid]);

  /**
   * حفظ الشخصية
   */
  const handleSave = useCallback(
    async (share: boolean = false) => {
      if (!isFormValid) {
        setError(tCommon("required"));
        return;
      }

      const setter = share ? setIsSavingShared : setIsSaving;
      setter(true);
      setError(null);

      try {
        if (isEditing && editPersona) {
          const success = await updatePersona(editPersona.id, {
            name: name.trim(),
            description: description.trim(),
            system_prompt: systemPrompt.trim(),
            icon_url: iconUrl,
            category,
          });

          if (success) {
            router.push(`/${locale}/personas`);
          } else {
            setError(tCommon("error_occurred"));
          }
        } else {
          const data: CreatePersonaData = {
            name: name.trim(),
            description: description.trim(),
            system_prompt: systemPrompt.trim(),
            icon_url: iconUrl,
            category,
            type: share ? "shared" : "custom",
          };

          const result = await createPersona(data);
          if (result) {
            router.push(`/${locale}/personas`);
          } else {
            setError(tCommon("error_occurred"));
          }
        }
      } catch {
        setError(tCommon("error_occurred"));
      } finally {
        setter(false);
      }
    },
    [
      isFormValid, isEditing, editPersona, name, description,
      systemPrompt, iconUrl, category, createPersona, updatePersona,
      router, locale, tCommon,
    ]
  );

  return (
    <>
      <div className="space-y-6">
        {/* الاسم */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {t("name_label")} <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => {
              setName(e.target.value.slice(0, 100));
              setError(null);
            }}
            placeholder={t("name_placeholder")}
            maxLength={100}
            className={cn(
              "w-full px-3 py-2.5 rounded-lg border text-sm",
              "bg-white dark:bg-dark-input",
              "border-gray-300 dark:border-dark-border",
              "focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
            )}
          />
          <p className="text-xs text-gray-400 text-end">{name.length}/100</p>
        </div>

        {/* الوصف */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {t("description_label")} <span className="text-red-500">*</span>
          </label>
          <textarea
            value={description}
            onChange={(e) => {
              setDescription(e.target.value);
              setError(null);
            }}
            placeholder={t("description_placeholder")}
            rows={2}
            className={cn(
              "w-full px-3 py-2.5 rounded-lg border text-sm resize-none",
              "bg-white dark:bg-dark-input",
              "border-gray-300 dark:border-dark-border",
              "focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
            )}
          />
        </div>

        {/* التصنيف */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {t("category_label")}
          </label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value as PersonaCategory)}
            className={cn(
              "w-full px-3 py-2.5 rounded-lg border text-sm",
              "bg-white dark:bg-dark-input",
              "border-gray-300 dark:border-dark-border",
              "focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
            )}
          >
            {PERSONA_CATEGORIES.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.icon} {locale === "ar" ? cat.labelAr : cat.labelEn}
              </option>
            ))}
          </select>
        </div>

        {/* الأيقونة */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {t("icon_label")}
          </label>
          <div className="relative">
            <button
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
              className={cn(
                "flex items-center gap-3 px-4 py-2.5 rounded-lg border w-full",
                "bg-white dark:bg-dark-input",
                "border-gray-300 dark:border-dark-border",
                "hover:border-primary/30 transition-colors"
              )}
            >
              <span className="text-2xl">{iconUrl}</span>
              <span className="text-sm text-gray-500">{t("icon_label")}</span>
            </button>

            {showEmojiPicker && (
              <div
                className={cn(
                  "absolute top-full mt-2 z-20 p-3 rounded-xl shadow-xl",
                  "bg-white dark:bg-dark-card",
                  "border border-gray-200 dark:border-dark-border",
                  "grid grid-cols-8 gap-1",
                  "animate-fade-in"
                )}
              >
                {EMOJI_OPTIONS.map((emoji) => (
                  <button
                    key={emoji}
                    onClick={() => {
                      setIconUrl(emoji);
                      setShowEmojiPicker(false);
                    }}
                    className={cn(
                      "h-9 w-9 rounded-lg text-xl",
                      "hover:bg-primary/10 transition-colors",
                      "flex items-center justify-center",
                      iconUrl === emoji && "bg-primary/20 ring-2 ring-primary"
                    )}
                  >
                    {emoji}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* التعليمات (System Prompt) */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {t("system_prompt_label")} <span className="text-red-500">*</span>
          </label>
          <textarea
            value={systemPrompt}
            onChange={(e) => {
              setSystemPrompt(e.target.value.slice(0, MAX_SYSTEM_PROMPT_LENGTH));
              setError(null);
            }}
            placeholder={t("system_prompt_placeholder")}
            rows={8}
            maxLength={MAX_SYSTEM_PROMPT_LENGTH}
            className={cn(
              "w-full px-3 py-2.5 rounded-lg border text-sm resize-y min-h-[120px]",
              "bg-white dark:bg-dark-input",
              "border-gray-300 dark:border-dark-border",
              "focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary",
              "font-mono text-xs leading-relaxed"
            )}
          />
          <div className="flex items-center justify-between">
            <p
              className={cn(
                "text-xs",
                promptLength < 10
                  ? "text-red-500"
                  : promptLength > MAX_SYSTEM_PROMPT_LENGTH * 0.9
                  ? "text-yellow-500"
                  : "text-gray-400"
              )}
            >
              {promptLength > 0 && !isPromptValid && "يجب 10 أحرف على الأقل"}
            </p>
            <p
              className={cn(
                "text-xs",
                promptLength > MAX_SYSTEM_PROMPT_LENGTH * 0.9
                  ? "text-yellow-500"
                  : "text-gray-400"
              )}
            >
              {promptLength}/{MAX_SYSTEM_PROMPT_LENGTH}
            </p>
          </div>
        </div>

        {/* الخطأ */}
        {error && (
          <div className="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-sm text-red-600 dark:text-red-400 animate-fade-in">
            {error}
          </div>
        )}

        {/* الأزرار */}
        <div className="flex items-center gap-3">
          {/* معاينة */}
          <button
            onClick={() => setShowPreview(true)}
            disabled={!isFormValid}
            className={cn(
              "flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium",
              "border border-gray-300 dark:border-dark-border",
              "text-gray-700 dark:text-gray-300",
              "hover:bg-gray-50 dark:hover:bg-dark-hover",
              "disabled:opacity-50 transition-colors"
            )}
          >
            <Eye className="h-4 w-4" />
            <span>{t("preview")}</span>
          </button>

          <div className="flex-1" />

          {/* حفظ */}
          <button
            onClick={() => handleSave(false)}
            disabled={!isFormValid || isSaving}
            className={cn(
              "flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium",
              "bg-primary hover:bg-primary-600 text-white",
              "disabled:opacity-50 transition-colors"
            )}
          >
            {isSaving ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Save className="h-4 w-4" />
            )}
            <span>{t("save")}</span>
          </button>

          {/* حفظ ومشاركة */}
          {!isEditing && (
            <button
              onClick={() => handleSave(true)}
              disabled={!isFormValid || isSavingShared}
              className={cn(
                "flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium",
                "bg-gradient-to-r from-primary to-secondary text-white",
                "hover:opacity-90 disabled:opacity-50 transition-opacity"
              )}
            >
              {isSavingShared ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Share2 className="h-4 w-4" />
              )}
              <span>{t("save_and_share")}</span>
            </button>
          )}
        </div>
      </div>

      {/* المعاينة */}
      {showPreview && (
        <PersonaPreview
          name={name}
          description={description}
          category={category}
          iconUrl={iconUrl}
          systemPrompt={systemPrompt}
          onClose={() => setShowPreview(false)}
          onConfirm={() => {
            setShowPreview(false);
            handleSave(false);
          }}
        />
      )}
    </>
  );
}
''')
    files_created += 1

    # 6. PersonaLibrary
    create_file("components/personas/PersonaLibrary.tsx", '''// مكتبة الشخصيات - 4 تبويبات مع بحث وتصفية وشبكة متجاوبة
"use client";

import { useState, useMemo, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { Plus, Search } from "lucide-react";

import PersonaCard from "@/components/personas/PersonaCard";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import EmptyState from "@/components/common/EmptyState";
import { usePersonas } from "@/hooks/usePersonas";
import { useAuthStore } from "@/stores/authStore";
import { useUIStore } from "@/stores/uiStore";
import { PERSONA_CATEGORIES } from "@/utils/constants";
import { debounce } from "@/utils/helpers";
import { cn } from "@/utils/cn";

import type { PersonaCategory } from "@/types/persona";

/**
 * التبويبات
 */
type TabKey = "basic" | "premium" | "custom" | "community";

/**
 * مكتبة الشخصيات مع التبويبات
 */
export default function PersonaLibrary() {
  const t = useTranslations("personas");
  const router = useRouter();
  const locale = useUIStore((s) => s.locale);
  const role = useAuthStore((s) => s.role);
  const {
    systemPersonas,
    premiumPersonas,
    customPersonas,
    communityPersonas,
    isLoading,
    canCreateCustom,
  } = usePersonas();

  const [activeTab, setActiveTab] = useState<TabKey>("basic");
  const [searchQuery, setSearchQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<PersonaCategory | "all">("all");

  const debouncedSetQuery = useMemo(
    () => debounce((q: string) => setDebouncedQuery(q), 300),
    []
  );

  const handleSearchChange = useCallback(
    (value: string) => {
      setSearchQuery(value);
      debouncedSetQuery(value);
    },
    [debouncedSetQuery]
  );

  /**
   * الشخصيات حسب التبويب النشط
   */
  const currentPersonas = useMemo(() => {
    switch (activeTab) {
      case "basic":
        return systemPersonas;
      case "premium":
        return premiumPersonas;
      case "custom":
        return customPersonas;
      case "community":
        return communityPersonas;
      default:
        return [];
    }
  }, [activeTab, systemPersonas, premiumPersonas, customPersonas, communityPersonas]);

  /**
   * تصفية حسب البحث والتصنيف
   */
  const filteredPersonas = useMemo(() => {
    let filtered = currentPersonas;

    if (debouncedQuery.trim()) {
      const q = debouncedQuery.toLowerCase();
      filtered = filtered.filter(
        (p) =>
          p.name.toLowerCase().includes(q) ||
          p.description.toLowerCase().includes(q)
      );
    }

    if (categoryFilter !== "all") {
      filtered = filtered.filter((p) => p.category === categoryFilter);
    }

    return filtered;
  }, [currentPersonas, debouncedQuery, categoryFilter]);

  const tabs: { key: TabKey; label: string; count: number }[] = [
    { key: "basic", label: t("tab_basic"), count: systemPersonas.length },
    { key: "premium", label: t("tab_premium"), count: premiumPersonas.length },
    { key: "custom", label: t("tab_custom"), count: customPersonas.length },
    { key: "community", label: t("tab_community"), count: communityPersonas.length },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 space-y-6">
      {/* التبويبات */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-gray-100 dark:bg-dark-surface overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => {
              setActiveTab(tab.key);
              setCategoryFilter("all");
            }}
            className={cn(
              "flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap",
              "transition-all duration-200",
              activeTab === tab.key
                ? "bg-white dark:bg-dark-card text-primary shadow-sm"
                : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
            )}
          >
            <span>{tab.label}</span>
            <span
              className={cn(
                "text-[10px] px-1.5 py-0.5 rounded-full",
                activeTab === tab.key
                  ? "bg-primary/10 text-primary"
                  : "bg-gray-200 dark:bg-dark-border text-gray-500"
              )}
            >
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* البحث + التصفية + إنشاء */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        {/* البحث */}
        <div className="relative flex-1">
          <Search className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => handleSearchChange(e.target.value)}
            placeholder={`${t("library_title")}...`}
            className={cn(
              "w-full ps-9 pe-3 py-2.5 rounded-lg border text-sm",
              "bg-white dark:bg-dark-input",
              "border-gray-300 dark:border-dark-border",
              "focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
            )}
          />
        </div>

        {/* فلتر التصنيف */}
        <select
          value={categoryFilter}
          onChange={(e) =>
            setCategoryFilter(e.target.value as PersonaCategory | "all")
          }
          className={cn(
            "px-3 py-2.5 rounded-lg border text-sm",
            "bg-white dark:bg-dark-input",
            "border-gray-300 dark:border-dark-border",
            "focus:outline-none focus:ring-2 focus:ring-primary/50"
          )}
        >
          <option value="all">{t("select_category")}</option>
          {PERSONA_CATEGORIES.map((cat) => (
            <option key={cat.value} value={cat.value}>
              {cat.icon} {locale === "ar" ? cat.labelAr : cat.labelEn}
            </option>
          ))}
        </select>

        {/* زر إنشاء (في تبويب المخصصة) */}
        {activeTab === "custom" && (
          <button
            onClick={() => router.push(`/${locale}/personas/create`)}
            disabled={!canCreateCustom}
            className={cn(
              "flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium",
              "bg-primary hover:bg-primary-600 text-white",
              "disabled:opacity-50 transition-colors whitespace-nowrap"
            )}
          >
            <Plus className="h-4 w-4" />
            <span>{t("create_title")}</span>
          </button>
        )}
      </div>

      {/* شبكة الشخصيات */}
      {filteredPersonas.length === 0 ? (
        <EmptyState
          title={t("library_title")}
          description={searchQuery ? undefined : undefined}
          action={
            activeTab === "custom" && canCreateCustom ? (
              <button
                onClick={() => router.push(`/${locale}/personas/create`)}
                className="px-4 py-2 rounded-lg bg-primary hover:bg-primary-600 text-white text-sm font-medium transition-colors"
              >
                {t("create_title")}
              </button>
            ) : undefined
          }
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredPersonas.map((persona) => (
            <PersonaCard key={persona.id} persona={persona} />
          ))}
        </div>
      )}
    </div>
  );
}
''')
    files_created += 1

    # 7. PersonaRating
    create_file("components/personas/PersonaRating.tsx", '''// تقييم الشخصية - 1 إلى 5 نجوم قابلة للنقر مع متوسط وعدد
"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { Star } from "lucide-react";

import { usePersonas } from "@/hooks/usePersonas";
import { cn } from "@/utils/cn";

/**
 * خصائص تقييم الشخصية
 */
interface PersonaRatingProps {
  personaId: string;
  averageRating: number;
  ratingCount: number;
  compact?: boolean;
  readOnly?: boolean;
}

/**
 * مكون تقييم الشخصية بالنجوم
 */
export default function PersonaRating({
  personaId,
  averageRating,
  ratingCount,
  compact = false,
  readOnly = false,
}: PersonaRatingProps) {
  const { ratePersona, getUserRating } = usePersonas();
  const [hoveredStar, setHoveredStar] = useState<number | null>(null);
  const [userRating, setUserRating] = useState<number | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isMountedRef = useRef(true);

  // جلب تقييم المستخدم عند التحميل
  useEffect(() => {
    isMountedRef.current = true;

    if (!readOnly) {
      getUserRating(personaId).then((rating) => {
        if (isMountedRef.current) setUserRating(rating);
      });
    }

    return () => {
      isMountedRef.current = false;
    };
  }, [personaId, getUserRating, readOnly]);

  /**
   * معالجة النقر على نجمة
   */
  const handleRate = useCallback(
    async (rating: number) => {
      if (readOnly || isSubmitting) return;

      setIsSubmitting(true);
      try {
        const success = await ratePersona(personaId, rating);
        if (success && isMountedRef.current) {
          setUserRating(rating);
        }
      } catch {
        // صامت
      } finally {
        if (isMountedRef.current) setIsSubmitting(false);
      }
    },
    [personaId, ratePersona, readOnly, isSubmitting]
  );

  const displayRating = hoveredStar ?? userRating ?? averageRating;

  if (compact) {
    return (
      <div className="flex items-center gap-1.5">
        <div className="flex items-center gap-0.5">
          {Array.from({ length: 5 }).map((_, i) => {
            const starValue = i + 1;
            const isFilled = starValue <= Math.round(displayRating);

            return (
              <button
                key={i}
                onClick={() => handleRate(starValue)}
                onMouseEnter={() => !readOnly && setHoveredStar(starValue)}
                onMouseLeave={() => setHoveredStar(null)}
                disabled={readOnly || isSubmitting}
                aria-label={`Rate ${starValue} stars`}
                className={cn(
                  "transition-colors disabled:cursor-default",
                  !readOnly && "cursor-pointer hover:scale-110"
                )}
              >
                <Star
                  className={cn(
                    "h-3 w-3",
                    isFilled
                      ? "text-yellow-500 fill-yellow-500"
                      : "text-gray-300 dark:text-gray-600"
                  )}
                />
              </button>
            );
          })}
        </div>
        <span className="text-[10px] text-gray-400 dark:text-gray-500">
          ({ratingCount})
        </span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <div className="flex items-center gap-1">
        {Array.from({ length: 5 }).map((_, i) => {
          const starValue = i + 1;
          const isFilled = starValue <= Math.round(displayRating);
          const isUserRated = userRating !== null && starValue <= userRating;

          return (
            <button
              key={i}
              onClick={() => handleRate(starValue)}
              onMouseEnter={() => !readOnly && setHoveredStar(starValue)}
              onMouseLeave={() => setHoveredStar(null)}
              disabled={readOnly || isSubmitting}
              aria-label={`Rate ${starValue} stars`}
              className={cn(
                "p-0.5 transition-all",
                !readOnly && "cursor-pointer hover:scale-125",
                "disabled:cursor-default"
              )}
            >
              <Star
                className={cn(
                  "h-5 w-5 transition-colors",
                  isFilled
                    ? isUserRated
                      ? "text-primary fill-primary"
                      : "text-yellow-500 fill-yellow-500"
                    : "text-gray-300 dark:text-gray-600"
                )}
              />
            </button>
          );
        })}
      </div>

      <div className="text-sm text-gray-500 dark:text-gray-400">
        <span className="font-semibold">{averageRating.toFixed(1)}</span>
        <span className="text-xs ms-1">({ratingCount})</span>
      </div>
    </div>
  );
}
''')
    files_created += 1

    # 8. PremiumPersonaLock
    create_file("components/personas/PremiumPersonaLock.tsx", '''// قفل الشخصية المميزة - تجربة مجانية أو ترقية
"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { Crown, X, Zap, Ticket, Loader2 } from "lucide-react";

import { usePersonas } from "@/hooks/usePersonas";
import { useUIStore } from "@/stores/uiStore";
import { cn } from "@/utils/cn";

import type { Persona } from "@/types/persona";

/**
 * خصائص مكون القفل المميز
 */
interface PremiumPersonaLockProps {
  persona: Persona;
  onClose: () => void;
}

/**
 * مكون قفل الشخصية المميزة - يعرض خيارات التجربة والترقية
 */
export default function PremiumPersonaLock({
  persona,
  onClose,
}: PremiumPersonaLockProps) {
  const t = useTranslations("personas");
  const tSettings = useTranslations("settings");
  const router = useRouter();
  const locale = useUIStore((s) => s.locale);
  const { checkTrialUsed, useTrialMessage, setActive } = usePersonas();

  const [trialUsed, setTrialUsed] = useState<boolean | null>(null);
  const [isActivating, setIsActivating] = useState(false);
  const isMountedRef = useRef(true);

  // التحقق من استخدام التجربة
  useEffect(() => {
    isMountedRef.current = true;

    checkTrialUsed(persona.id).then((used) => {
      if (isMountedRef.current) setTrialUsed(used);
    });

    return () => {
      isMountedRef.current = false;
    };
  }, [persona.id, checkTrialUsed]);

  /**
   * تفعيل الرسالة التجريبية
   */
  const handleTrialActivation = useCallback(async () => {
    setIsActivating(true);
    try {
      const success = await useTrialMessage(persona.id);
      if (success) {
        setActive(persona);
        onClose();
      } else {
        if (isMountedRef.current) setTrialUsed(true);
      }
    } catch {
      // صامت
    } finally {
      if (isMountedRef.current) setIsActivating(false);
    }
  }, [persona, useTrialMessage, setActive, onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* خلفية معتمة */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* المحتوى */}
      <div
        className={cn(
          "relative w-full max-w-sm mx-4",
          "bg-white dark:bg-dark-card",
          "rounded-2xl shadow-2xl",
          "border border-gray-200 dark:border-dark-border",
          "p-6",
          "animate-fade-in"
        )}
      >
        {/* زر الإغلاق */}
        <button
          onClick={onClose}
          aria-label="Close"
          className="absolute top-4 end-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        <div className="flex flex-col items-center text-center space-y-5">
          {/* الأيقونة */}
          <div
            className={cn(
              "h-16 w-16 rounded-2xl",
              "bg-gradient-to-br from-yellow-400 to-yellow-600",
              "flex items-center justify-center",
              "shadow-lg shadow-yellow-500/30"
            )}
          >
            <Crown className="h-8 w-8 text-white" />
          </div>

          {/* العنوان */}
          <div className="space-y-2">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
              {persona.name}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {t("upgrade_prompt")}
            </p>
          </div>

          {/* الخيارات */}
          <div className="w-full space-y-3">
            {/* تجربة مجانية */}
            {trialUsed === false && (
              <button
                onClick={handleTrialActivation}
                disabled={isActivating}
                className={cn(
                  "w-full flex items-center justify-center gap-2",
                  "px-4 py-3 rounded-xl text-sm font-medium",
                  "bg-gradient-to-r from-primary to-secondary text-white",
                  "hover:opacity-90 disabled:opacity-50 transition-opacity"
                )}
              >
                {isActivating ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Zap className="h-4 w-4" />
                )}
                <span>{t("trial_message_button")}</span>
              </button>
            )}

            {/* تم استخدام التجربة */}
            {trialUsed === true && (
              <p className="text-xs text-gray-400 dark:text-gray-500 italic">
                {t("trial_used")}
              </p>
            )}

            {/* جاري التحقق */}
            {trialUsed === null && (
              <div className="flex justify-center py-2">
                <Loader2 className="h-5 w-5 animate-spin text-primary" />
              </div>
            )}

            {/* فاصل */}
            <div className="flex items-center gap-3">
              <div className="flex-1 border-t border-gray-200 dark:border-dark-border" />
              <span className="text-xs text-gray-400">أو</span>
              <div className="flex-1 border-t border-gray-200 dark:border-dark-border" />
            </div>

            {/* ترقية عبر التجربة المجانية */}
            <button
              onClick={() => {
                onClose();
                router.push(`/${locale}/settings`);
              }}
              className={cn(
                "w-full flex items-center justify-center gap-2",
                "px-4 py-3 rounded-xl text-sm font-medium",
                "border border-primary text-primary",
                "hover:bg-primary/5 transition-colors"
              )}
            >
              <Crown className="h-4 w-4" />
              <span>{tSettings("trial_button")}</span>
            </button>

            {/* إدخال رمز دعوة */}
            <button
              onClick={() => {
                onClose();
                router.push(`/${locale}/settings`);
              }}
              className={cn(
                "w-full flex items-center justify-center gap-2",
                "px-4 py-3 rounded-xl text-sm font-medium",
                "border border-gray-300 dark:border-dark-border",
                "text-gray-600 dark:text-gray-400",
                "hover:bg-gray-50 dark:hover:bg-dark-hover transition-colors"
              )}
            >
              <Ticket className="h-4 w-4" />
              <span>{tSettings("invite_code_label")}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
''')
    files_created += 1

    # 9. PersonaPreview
    create_file("components/personas/PersonaPreview.tsx", '''// معاينة الشخصية - عرض البطاقة قبل الحفظ مع تأكيد
"use client";

import { useTranslations } from "next-intl";
import { Check, X } from "lucide-react";

import { PERSONA_CATEGORIES } from "@/utils/constants";
import { useUIStore } from "@/stores/uiStore";
import { cn } from "@/utils/cn";

import type { PersonaCategory } from "@/types/persona";

/**
 * خصائص المعاينة
 */
interface PersonaPreviewProps {
  name: string;
  description: string;
  category: PersonaCategory;
  iconUrl: string;
  systemPrompt: string;
  onClose: () => void;
  onConfirm: () => void;
}

/**
 * معاينة الشخصية قبل الحفظ
 */
export default function PersonaPreview({
  name,
  description,
  category,
  iconUrl,
  systemPrompt,
  onClose,
  onConfirm,
}: PersonaPreviewProps) {
  const t = useTranslations("personas");
  const tCommon = useTranslations("common");
  const locale = useUIStore((s) => s.locale);

  const categoryInfo = PERSONA_CATEGORIES.find((c) => c.value === category);
  const truncatedPrompt =
    systemPrompt.length > 100
      ? systemPrompt.slice(0, 100) + "..."
      : systemPrompt;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* خلفية معتمة */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* المحتوى */}
      <div
        className={cn(
          "relative w-full max-w-md mx-4",
          "bg-white dark:bg-dark-card",
          "rounded-2xl shadow-2xl",
          "border border-gray-200 dark:border-dark-border",
          "overflow-hidden",
          "animate-fade-in"
        )}
      >
        {/* الرأس المتدرج */}
        <div
          className={cn(
            "bg-gradient-to-br from-primary/10 to-secondary/10",
            "dark:from-primary/20 dark:to-secondary/20",
            "px-6 py-8"
          )}
        >
          <div className="flex flex-col items-center text-center gap-3">
            <div
              className={cn(
                "h-16 w-16 rounded-2xl",
                "bg-white dark:bg-dark-card",
                "shadow-lg",
                "flex items-center justify-center text-3xl"
              )}
            >
              {iconUrl}
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                {name || "..."}
              </h3>
              {categoryInfo && (
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {categoryInfo.icon}{" "}
                  {locale === "ar" ? categoryInfo.labelAr : categoryInfo.labelEn}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* الوصف و System Prompt */}
        <div className="px-6 py-5 space-y-4">
          {/* الوصف */}
          <div>
            <p className="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase mb-1">
              {t("description_label")}
            </p>
            <p className="text-sm text-gray-700 dark:text-gray-300">
              {description || "..."}
            </p>
          </div>

          {/* معاينة System Prompt */}
          <div>
            <p className="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase mb-1">
              {t("system_prompt_label")}
            </p>
            <div
              className={cn(
                "p-3 rounded-lg",
                "bg-gray-50 dark:bg-dark-surface",
                "border border-gray-100 dark:border-dark-border"
              )}
            >
              <p className="text-xs text-gray-600 dark:text-gray-400 font-mono leading-relaxed">
                {truncatedPrompt || "..."}
              </p>
            </div>
          </div>
        </div>

        {/* الأزرار */}
        <div
          className={cn(
            "flex items-center gap-3 px-6 py-4",
            "border-t border-gray-200 dark:border-dark-border"
          )}
        >
          <button
            onClick={onClose}
            className={cn(
              "flex-1 flex items-center justify-center gap-2",
              "px-4 py-2.5 rounded-lg text-sm font-medium",
              "border border-gray-300 dark:border-dark-border",
              "text-gray-700 dark:text-gray-300",
              "hover:bg-gray-50 dark:hover:bg-dark-hover",
              "transition-colors"
            )}
          >
            <X className="h-4 w-4" />
            <span>{tCommon("cancel")}</span>
          </button>
          <button
            onClick={onConfirm}
            className={cn(
              "flex-1 flex items-center justify-center gap-2",
              "px-4 py-2.5 rounded-lg text-sm font-medium",
              "bg-primary hover:bg-primary-600 text-white",
              "transition-colors"
            )}
          >
            <Check className="h-4 w-4" />
            <span>{t("save")}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
''')
    files_created += 1

    # 10. ErrorMessage (update)
    create_file("components/common/ErrorMessage.tsx", '''// مكون رسالة الخطأ - أيقونة حمراء ونص مع خيار إعادة المحاولة
"use client";

import { AlertTriangle, RefreshCw } from "lucide-react";

import { cn } from "@/utils/cn";

/**
 * خصائص رسالة الخطأ
 */
interface ErrorMessageProps {
  /** نص رسالة الخطأ */
  message: string;
  /** عنوان الخطأ (اختياري) */
  title?: string;
  /** دالة إعادة المحاولة (اختياري) */
  onRetry?: () => void;
  /** نص زر إعادة المحاولة */
  retryLabel?: string;
  /** حجم المكون */
  size?: "sm" | "md" | "lg";
  /** أصناف CSS إضافية */
  className?: string;
}

/**
 * رسالة خطأ موحدة مع خيار إعادة المحاولة
 */
export default function ErrorMessage({
  message,
  title,
  onRetry,
  retryLabel = "حاول مرة أخرى",
  size = "md",
  className,
}: ErrorMessageProps) {
  const sizeClasses = {
    sm: "px-3 py-2 text-xs",
    md: "px-4 py-3 text-sm",
    lg: "px-5 py-4 text-base",
  };

  const iconSizes = {
    sm: "h-4 w-4",
    md: "h-5 w-5",
    lg: "h-6 w-6",
  };

  return (
    <div
      className={cn(
        "rounded-lg border",
        "border-red-200 dark:border-red-800/50",
        "bg-red-50 dark:bg-red-900/20",
        sizeClasses[size],
        "animate-fade-in",
        className
      )}
      role="alert"
    >
      <div className="flex items-start gap-3">
        <AlertTriangle
          className={cn(
            "text-red-500 dark:text-red-400 shrink-0 mt-0.5",
            iconSizes[size]
          )}
        />
        <div className="flex-1 space-y-1">
          {title && (
            <h4
              className={cn(
                "font-medium text-red-800 dark:text-red-300",
                size === "sm" ? "text-xs" : size === "lg" ? "text-base" : "text-sm"
              )}
            >
              {title}
            </h4>
          )}
          <p
            className={cn(
              "text-red-600 dark:text-red-400",
              size === "sm" ? "text-xs" : size === "lg" ? "text-sm" : "text-sm"
            )}
          >
            {message}
          </p>
        </div>
      </div>

      {onRetry && (
        <button
          onClick={onRetry}
          className={cn(
            "mt-3 flex items-center gap-1.5",
            "font-medium text-red-600 dark:text-red-400",
            "hover:text-red-700 dark:hover:text-red-300",
            "transition-colors",
            size === "sm" ? "text-xs" : "text-sm"
          )}
        >
          <RefreshCw className={cn(size === "sm" ? "h-3 w-3" : "h-3.5 w-3.5")} />
          <span>{retryLabel}</span>
        </button>
      )}
    </div>
  );
}
''')
    files_created += 1

    # ──────────────────────────────────────────────
    # SUMMARY
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("✅ Phase 5B Complete!")
    print("=" * 60)
    print(f"\n📊 Total files created: {files_created}")
    print("\n📁 Files created:")
    print("   HOOKS (1 file):")
    print("     1.  hooks/usePersonas.ts                    - Full personas CRUD + rate + trial")
    print("   PAGES (2 files):")
    print("     2.  app/[locale]/personas/page.tsx           - Persona library page")
    print("     3.  app/[locale]/personas/create/page.tsx    - Create persona page")
    print("   PERSONA COMPONENTS (6 files):")
    print("     4.  components/personas/PersonaCard.tsx       - Card with use/copy/star")
    print("     5.  components/personas/PersonaForm.tsx        - Create/edit form")
    print("     6.  components/personas/PersonaLibrary.tsx     - 4-tab library with search")
    print("     7.  components/personas/PersonaRating.tsx      - 1-5 star rating")
    print("     8.  components/personas/PremiumPersonaLock.tsx - Trial/upgrade dialog")
    print("     9.  components/personas/PersonaPreview.tsx     - Preview before save")
    print("   COMMON (1 file):")
    print("     10. components/common/ErrorMessage.tsx         - Error with retry")
    print("\n📝 Key Features:")
    print("   - usePersonas: full CRUD, share+notify, rate(1-5), copy, trial check/use")
    print("   - create: limit 4 for free, shared type triggers notification")
    print("   - PersonaCard: active highlight, premium lock, copy, favorite toggle")
    print("   - PersonaForm: name(100), emoji picker, category, char counter, preview")
    print("   - PersonaLibrary: 4 tabs (basic/premium/custom/community), search, category filter")
    print("   - PersonaLibrary: responsive grid 1/2/3/4 cols")
    print("   - PersonaRating: clickable stars, hover, user rating highlighted in primary")
    print("   - PremiumPersonaLock: trial button if !used, upgrade via trial/invite code")
    print("   - PersonaPreview: icon+name+desc+category+100char prompt, confirm/cancel")
    print("   - All: TypeScript strict, no any, Tailwind only, i18n, RTL/LTR")
    print("\n📋 Cumulative files: ~97 | Remaining: ~33")
    print("\n🔜 Next: Phase 6A - Admin Dashboard, Users Table, API Keys Management")

if __name__ == "__main__":
    main()
